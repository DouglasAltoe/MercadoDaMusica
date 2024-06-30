import json
import sqlite3
from typing import Optional
from models.genero_model import Genero
from sql.genero_sql import *
from util.database import obter_conexao


class GeneroRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, genero: Genero) -> Optional[Genero]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR,
                    (genero.descricao),
                )
                if cursor.rowcount > 0:
                    genero.id = cursor.lastrowid
                    return genero
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def inserir_generos_json(cls, arquivo_json: str):
        if GeneroRepo.obter_quantidade() == 0:
            with open(arquivo_json, "r", encoding="utf-8") as arquivo:
                generos = json.load(arquivo)
                for genero in generos:
                    GeneroRepo.inserir(Genero(**genero))

    @classmethod
    def obter_quantidade(cls) -> Optional[int]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_QUANTIDADE).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return None