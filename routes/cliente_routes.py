from datetime import datetime
from fastapi import APIRouter, Form, Query, Request, status
from fastapi.responses import JSONResponse, RedirectResponse

from dtos.alterar_cliente_dto import AlterarClienteDTO
from dtos.alterar_senha_dto import AlterarSenhaDTO
from models.cliente_model import Cliente
from models.item_pedido_model import ItemPedido
from models.pedido_model import Pedido
from repositories.cliente_repo import ClienteRepo
from repositories.item_pedido_repo import ItemPedidoRepo
from repositories.pedido_repo import PedidoRepo
from repositories.musica_repo import MusicaRepo
from util.auth import conferir_senha, obter_hash_senha
from util.cookies import (
    adicionar_mensagem_alerta,
    adicionar_mensagem_erro,
    adicionar_mensagem_sucesso,
    excluir_cookie_auth,
)
from util.templates import obter_jinja_templates

router = APIRouter(prefix="/cliente")
templates = obter_jinja_templates("templates/cliente")


@router.get("/pedidos")
async def get_pedidos(request: Request):
    return templates.TemplateResponse(
        "pages/pedidos.html",
        {"request": request},
    )


@router.get("/cadastro")
async def get_cadastro(request: Request):
    return templates.TemplateResponse(
        "pages/cadastro.html",
        {
            "request": request,
        },
    )


@router.post("/post_cadastro", response_class=JSONResponse)
async def post_cadastro(request: Request, alterar_dto: AlterarClienteDTO):
    id = request.state.cliente.id
    cliente_data = alterar_dto.model_dump()
    response = JSONResponse({"redirect": {"url": "/cliente/cadastro"}})
    if ClienteRepo.alterar(Cliente(id, **cliente_data)):
        adicionar_mensagem_sucesso(response, "Cadastro alterado com sucesso!")
    else:
        adicionar_mensagem_erro(
            response, "Não foi possível alterar os dados cadastrais!"
        )
    return response


@router.get("/senha")
async def get_senha(request: Request):
    return templates.TemplateResponse(
        "pages/senha.html",
        {"request": request},
    )


@router.post("/post_senha", response_class=JSONResponse)
async def post_senha(request: Request, alterar_dto: AlterarSenhaDTO):
    email = request.state.cliente.email
    cliente_bd = ClienteRepo.obter_por_email(email)
    nova_senha_hash = obter_hash_senha(alterar_dto.nova_senha)
    response = JSONResponse({"redirect": {"url": "/cliente/senha"}})
    if not conferir_senha(alterar_dto.senha, cliente_bd.senha):
        adicionar_mensagem_erro(response, "Senha atual incorreta!")
        return response
    if ClienteRepo.alterar_senha(cliente_bd.id, nova_senha_hash):
        adicionar_mensagem_sucesso(response, "Senha alterada com sucesso!")
    else:
        adicionar_mensagem_erro(response, "Não foi possível alterar sua senha!")
    return response



@router.get("/sair", response_class=RedirectResponse)
async def get_sair(request: Request):
    if request.state.cliente:
        ClienteRepo.alterar_token(request.state.cliente.email, "")
    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    excluir_cookie_auth(response)
    adicionar_mensagem_sucesso(response, "Saída realizada com sucesso!")
    return response

@router.get("/cartaoform")
async def get_cartaoform(request: Request):
    return templates.TemplateResponse(
        "pages/cartaoform.html",
        {"request": request},
    )


@router.get("/carrinho")
async def get_carrinho(request: Request, id_musica: int = Query(0)):
    
    
    pedidos = PedidoRepo.obter_por_estado(request.state.cliente.id, 1)
    pedido_carrinho = pedidos[0] if pedidos else None
    if pedido_carrinho:
        itens_pedido = ItemPedidoRepo.obter_por_pedido(pedido_carrinho.id)
    return templates.TemplateResponse(
        "pages/carrinho.html",
        {"request": request, "itens": itens_pedido},
    )

@router.post("/post_adicionar_carrinho", response_class=RedirectResponse)
async def post_adicionar_carrinho(request: Request, id_musica: int = Form(...)):
    musica = MusicaRepo.obter_um(id_musica)
    mensagem = f"A música <b>{musica.nome}</b> foi adicionada ao carrinho."    
    pedidos = PedidoRepo.obter_por_estado(request.state.cliente.id, 1)
    pedido_carrinho = pedidos[0] if pedidos else None        
    if pedido_carrinho == None:
        pedido_carrinho = Pedido(0, datetime.now(), 0, request.state.cliente.endereco, 1, request.state.cliente.id)
        pedido_carrinho = PedidoRepo.inserir(pedido_carrinho)
    qtde = ItemPedidoRepo.obter_quantidade_por_musica(pedido_carrinho.id, id_musica)
    if qtde == 0:            
        item_pedido = ItemPedido(pedido_carrinho.id, id_musica, musica.nome, musica.preco, 1, 0)
        ItemPedidoRepo.inserir(item_pedido)            
    else:
        ItemPedidoRepo.aumentar_quantidade_musica(pedido_carrinho.id, id_musica)
        mensagem = f"A música <b>{musica.nome}</b> já estava no carrinho e teve sua quantidade aumentada."        
    response = RedirectResponse("/cliente/carrinho", status.HTTP_303_SEE_OTHER)
    adicionar_mensagem_sucesso(response, mensagem)
    return response

@router.post("/post_aumentar_item", response_class=RedirectResponse)
async def post_aumentar_item(request: Request, id_musica: int = Form(0)):
    musica = MusicaRepo.obter_um(id_musica)
    pedidos = PedidoRepo.obter_por_estado(request.state.cliente.id, 1)
    pedido_carrinho = pedidos[0] if pedidos else None
    
    if pedido_carrinho == None:
        response = RedirectResponse(f"/musica?id={id_musica}", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_alerta(f"Seu carrinho não foi encontrado. Adicione esta música ao carrinho novamente.")
        return response

    qtde = ItemPedidoRepo.obter_quantidade_por_musica(pedido_carrinho.id, id_musica)
    if qtde == 0:
        response = RedirectResponse(f"/musica?id={id_musica}", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_alerta(f"Esta música não foi encontrada em seu carrinho. Adicione-a novamente.")
        return response
    
    ItemPedidoRepo.aumentar_quantidade_musica(pedido_carrinho.id, id_musica)
    response = RedirectResponse("/cliente/carrinho", status.HTTP_303_SEE_OTHER)
    adicionar_mensagem_sucesso(response, f"A música <b>{musica.nome}</b> teve sua quantidade aumentada para <b>{qtde+1}</b>.")
    return response

@router.post("/post_reduzir_item", response_class=RedirectResponse)
async def post_reduzir_item(request: Request, id_musica: int = Form(0)):
    musica = MusicaRepo.obter_um(id_musica)
    pedidos = PedidoRepo.obter_por_estado(request.state.cliente.id, 1)
    pedido_carrinho = pedidos[0] if pedidos else None
    response = RedirectResponse("/cliente/carrinho", status.HTTP_303_SEE_OTHER)
    
    if pedido_carrinho == None:        
        adicionar_mensagem_alerta(f"Seu carrinho não foi encontrado.")
        return response

    qtde = ItemPedidoRepo.obter_quantidade_por_musica(pedido_carrinho.id, id_musica)
    if qtde == 0:        
        adicionar_mensagem_alerta(f"A música {id_musica} não foi encontrada em seu carrinho.")
        return response
    
    if qtde == 1:
        ItemPedidoRepo.excluir(pedido_carrinho.id, id_musica)        
        adicionar_mensagem_sucesso(response, f"A música <b>{musica.nome}</b> foi excluída do carrinho.")
        return response
    
    ItemPedidoRepo.diminuir_quantidade_musica(pedido_carrinho.id, id_musica)    
    adicionar_mensagem_sucesso(response, f"A música <b>{musica.nome}</b> teve sua quantidade diminuída para <b>{qtde+1}</b>.")
    return response


@router.post("/post_pagamento", response_class=RedirectResponse)
async def post_reduzir_item(request: Request):
    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    adicionar_mensagem_sucesso(response, f"O pagamento foi realizado com sucesso!")
    return response