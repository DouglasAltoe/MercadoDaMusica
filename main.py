from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from repositories.cliente_repo import ClienteRepo
from repositories.genero_repo import GeneroRepo
from repositories.item_pedido_repo import ItemPedidoRepo
from repositories.pedido_repo import PedidoRepo
from repositories.musica_repo import MusicaRepo
from routes import main_routes, cliente_routes
from util.auth import checar_permissao, middleware_autenticacao
from util.exceptions import configurar_excecoes

MusicaRepo.criar_tabela()
MusicaRepo.inserir_musicas_json("sql/musicas.json")
GeneroRepo.criar_tabela()
GeneroRepo.inserir_generos_json("sql/generos.json")
ClienteRepo.criar_tabela()
ClienteRepo.inserir_clientes_json("sql/clientes.json")
PedidoRepo.criar_tabela()
ItemPedidoRepo.criar_tabela()
app = FastAPI(dependencies=[Depends(checar_permissao)])
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
app.middleware(middleware_type="http")(middleware_autenticacao)
configurar_excecoes(app)
app.include_router(main_routes.router)
app.include_router(cliente_routes.router)
