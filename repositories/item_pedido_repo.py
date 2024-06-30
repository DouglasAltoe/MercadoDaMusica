import sqlite3
from typing import List, Optional
from models.item_pedido_model import ItemPedido
from sql.item_pedido_sql import *
from util.database import obter_conexao


class ItemPedidoRepo:
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, item_pedido: ItemPedido) -> Optional[ItemPedido]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR,
                    (
                        item_pedido.id_pedido,
                        item_pedido.id_musica,
                        item_pedido.nome_musica,
                        item_pedido.valor_musica,
                        item_pedido.quantidade,
                    ),
                )
                if cursor.rowcount > 0:
                    item_pedido.id = cursor.lastrowid
                    return item_pedido
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_por_pedido(cls, id_pedido: int) -> List[ItemPedido]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(
                    SQL_OBTER_POR_PEDIDO,
                    (id_pedido,),
                ).fetchall()
                itens_pedido = [ItemPedido(*t) for t in tuplas]
                return itens_pedido
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_quantidade_por_musica(
        cls, id_pedido: int, id_musica: int
    ) -> Optional[int]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(
                    SQL_OBTER_QUANTIDADE_POR_PRODUTO, (id_pedido, id_musica)
                ).fetchone()
                quantidade = int(tupla[0]) if tupla else 0
                return quantidade
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_quantidade_por_pedido(cls, id_pedido: int) -> Optional[int]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(
                    SQL_OBTER_QUANTIDADE_POR_PEDIDO, (id_pedido,)
                ).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def alterar_valor_musica(
        cls, id_pedido: int, id_musica: int, novo_valor: float
    ) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR_VALOR_PRODUTO,
                    (
                        novo_valor,
                        id_pedido,
                        id_musica,
                    ),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def alterar_quantidade_musica(
        cls, id_pedido: int, id_musica: int, nova_quantidade: int
    ) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR_QUANTIDADE_PRODUTO,
                    (
                        nova_quantidade,
                        id_pedido,
                        id_musica,
                    ),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def aumentar_quantidade_musica(cls, id_pedido: int, id_musica: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_AUMENTAR_QUANTIDADE_PRODUTO,
                    (                        
                        id_pedido,
                        id_musica,
                    ),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False
        
    @classmethod
    def diminuir_quantidade_musica(cls, id_pedido: int, id_musica: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_DIMINUIR_QUANTIDADE_PRODUTO,
                    (                        
                        id_pedido,
                        id_musica,
                    ),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False
    
    @classmethod
    def excluir(cls, id_pedido: int, id_musica: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_EXCLUIR,
                    (
                        id_pedido,
                        id_musica,
                    ),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False
