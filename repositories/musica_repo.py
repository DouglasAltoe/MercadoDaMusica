import json
import sqlite3
from typing import List, Optional
from models.musica_model import Musica
from sql.musica_sql import *
from util.database import obter_conexao
import shutil
from pathlib import Path


class MusicaRepo:
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, musica: Musica) -> Optional[Musica]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR,
                    (musica.nome, musica.artista, musica.preco, musica.descricao, musica.genero),
                )
                if cursor.rowcount > 0:
                    musica.id = cursor.lastrowid
                    return musica
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_todos(cls) -> List[Musica]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS).fetchall()
                musicas = [Musica(*t) for t in tuplas]
                return musicas
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def alterar(cls, musica: Musica) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR,
                    (
                        musica.nome,
                        musica.artista,
                        musica.preco,
                        musica.descricao,
                        musica.genero,
                        musica.id,
                    ),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def excluir(cls, id: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR, (id,))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def obter_um(cls, id: int) -> Optional[Musica]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_UM, (id,)).fetchone()
                musica = Musica(*tupla)
                return musica
        except sqlite3.Error as ex:
            print(ex)
            return None

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

    @classmethod
    def obter_busca(
        cls, termo: str, pagina: int, tamanho_pagina: int, ordem: int
    ) -> List[Musica]:
        termo = "%" + termo + "%"
        offset = (pagina - 1) * tamanho_pagina
        match (ordem):
            case 1:
                SQL_OBTER_BUSCA_ORDENADA = SQL_OBTER_BUSCA.replace("#1", "nome")
            case 2:
                SQL_OBTER_BUSCA_ORDENADA = SQL_OBTER_BUSCA.replace("#1", "genero ASC")
            case 3:
                SQL_OBTER_BUSCA_ORDENADA = SQL_OBTER_BUSCA.replace("#1", "artista")
            case _:
                SQL_OBTER_BUSCA_ORDENADA = SQL_OBTER_BUSCA.replace("#1", "nome")
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(
                    SQL_OBTER_BUSCA_ORDENADA, (termo, termo, tamanho_pagina, offset)
                ).fetchall()
                musicas = [Musica(*t) for t in tuplas]
                return musicas
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_quantidade_busca(cls, termo: str) -> Optional[int]:
        termo = "%" + termo + "%"
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(
                    SQL_OBTER_QUANTIDADE_BUSCA, (termo, termo)
                ).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def inserir_musicas_json(cls, arquivo_json: str):
        if MusicaRepo.obter_quantidade() == 0:
            with open(arquivo_json, "r", encoding="utf-8") as arquivo:
                musicas = json.load(arquivo)
                for musica in musicas:
                    MusicaRepo.inserir(Musica(**musica))
            cls.transferir_imagens("/static/img/musicas/inserir", "/static/img/musicas")

    @classmethod
    def transferir_imagens(cls, pasta_origem, pasta_destino):
        path_origem = Path(pasta_origem)
        path_destino = Path(pasta_destino)
        if not path_origem.exists() or not path_origem.is_dir():
            print(f"Pasta de origem {pasta_origem} não existe ou não é um diretório.")
            return
        if not path_destino.exists() or not path_destino.is_dir():
            print(f"Pasta de destino {pasta_destino} não existe ou não é um diretório.")
            return
        for arquivo_imagem in path_origem.glob("*"):
            if arquivo_imagem.is_file():
                path_arquivo_destino = path_destino / arquivo_imagem.name
                shutil.copy2(arquivo_imagem, path_arquivo_destino)
