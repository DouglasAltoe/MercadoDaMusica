import math
from sqlite3 import DatabaseError
from fastapi import APIRouter, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from dtos.entrar_dto import EntrarDTO
from util.html import ler_html
from dtos.novo_cliente_dto import NovoClienteDTO
from models.cliente_model import Cliente
from repositories.cliente_repo import ClienteRepo
from repositories.musica_repo import MusicaRepo
from util.auth import (
    conferir_senha,
    gerar_token,
    obter_hash_senha,
)

from util.cookies import adicionar_cookie_auth, adicionar_mensagem_sucesso
from util.pydantic import create_validation_errors
from util.templates import obter_jinja_templates

router = APIRouter()
templates = obter_jinja_templates("templates/main")


@router.get("/html/{arquivo}")
async def get_html(arquivo: str):
    response = HTMLResponse(ler_html(arquivo))
    return response


@router.get("/")
async def get_root(request: Request):
    musicas = MusicaRepo.obter_todos()
    return templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request,
            "musicas": musicas,
        },
    )


@router.get("/contato")
async def get_contato(request: Request):
    return templates.TemplateResponse(
        "pages/contato.html",
        {"request": request},
    )

@router.get("/sobre")
async def get_sobre(request: Request):
    return templates.TemplateResponse(
        "pages/sobre.html",
        {"request": request},
    )


@router.get("/cadastro")
async def get_cadastro(request: Request):
    return templates.TemplateResponse(
        "pages/cadastro.html",
        {"request": request},
    )


@router.post("/post_cadastro", response_class=JSONResponse)
async def post_cadastro(cliente_dto: NovoClienteDTO):
    cliente_data = cliente_dto.model_dump(exclude={"confirmacao_senha"})
    cliente_data["senha"] = obter_hash_senha(cliente_data["senha"])
    novo_cliente = ClienteRepo.inserir(Cliente(**cliente_data))
    if not novo_cliente or not novo_cliente.id:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar cliente.")
    return {"redirect": {"url": "/cadastro_realizado"}}


@router.get("/cadastro_realizado")
async def get_cadastro_realizado(request: Request):
    return templates.TemplateResponse(
        "pages/cadastro_confirmado.html",
        {"request": request},
    )


@router.get("/entrar")
async def get_entrar(
    request: Request,
    return_url: str = Query("/"),
):
    return templates.TemplateResponse(
        "pages/entrar.html",
        {
            "request": request,
            "return_url": return_url,
        },
    )


@router.post("/post_entrar", response_class=JSONResponse)
async def post_entrar(entrar_dto: EntrarDTO):
    cliente_entrou = ClienteRepo.obter_por_email(entrar_dto.email)
    if (
        (not cliente_entrou)
        or (not cliente_entrou.senha)
        or (not conferir_senha(entrar_dto.senha, cliente_entrou.senha))
    ):
        return JSONResponse(
            content=create_validation_errors(
                entrar_dto,
                ["email", "senha"],
                ["Credenciais inválidas.", "Credenciais inválidas."],
            ),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    token = gerar_token()
    if not ClienteRepo.alterar_token(cliente_entrou.id, token):
        raise DatabaseError(
            "Não foi possível alterar o token do cliente no banco de dados."
        )
    response = JSONResponse(content={"redirect": {"url": entrar_dto.return_url}})
    adicionar_mensagem_sucesso(
        response,
        f"Olá, <b>{cliente_entrou.nome}</b>. Seja bem-vindo(a) ao Mercado da Música!",
    )
    adicionar_cookie_auth(response, token)
    return response


@router.get("/musica/{id:int}")
async def get_musica(request: Request, id: int):
    musica = MusicaRepo.obter_um(id)
    return templates.TemplateResponse(
        "pages/musica.html",
        {
            "request": request,
            "musica": musica,
        },
    )


@router.get("/buscar")
async def get_buscar(
    request: Request,
    q: str,
    p: int = 1,
    tp: int = 6,
    o: int = 1,
):
    musicas = MusicaRepo.obter_busca(q, p, tp, o)
    qtde_musicas = MusicaRepo.obter_quantidade_busca(q)
    qtde_paginas = math.ceil(qtde_musicas / float(tp))
    return templates.TemplateResponse(
        "pages/buscar.html",
        {
            "request": request,
            "musicas": musicas,
            "quantidade_paginas": qtde_paginas,
            "tamanho_pagina": tp,
            "pagina_atual": p,
            "termo_busca": q,
            "ordem": o,
        },
    )
