SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS item_pedido (
        id_pedido INTEGER NOT NULL,
        id_musica INTEGER NOT NULL,
        nome_musica TEXT NOT NULL,
        valor_musica FLOAT NOT NULL,
        quantidade INTEGER NOT NULL,
        valor_item AS (valor_musica * quantidade),
        PRIMARY KEY(id_pedido, id_musica),
        FOREIGN KEY (id_pedido) REFERENCES pedido(id),
        FOREIGN KEY (id_musica) REFERENCES musica(id))
"""

SQL_INSERIR = """
    INSERT INTO item_pedido(id_pedido, id_musica, nome_musica, valor_musica, quantidade)
    VALUES (?, ?, ?, ?, ?)
"""

SQL_OBTER_POR_PEDIDO = """
    SELECT id_pedido, id_musica, nome_musica, valor_musica, quantidade, valor_item
    FROM item_pedido
    WHERE id_pedido=?
"""

SQL_OBTER_QUANTIDADE_POR_PRODUTO = """
    SELECT quantidade
    FROM item_pedido
    WHERE id_pedido=? AND id_musica=?
"""

SQL_ALTERAR_VALOR_PRODUTO = """
    UPDATE item_pedido
    SET valor_musica=?
    WHERE id_pedido=? AND id_musica=?
"""

SQL_ALTERAR_QUANTIDADE_PRODUTO = """
    UPDATE item_pedido
    SET quantidade=?
    WHERE id_pedido=? AND id_musica=?
"""

SQL_AUMENTAR_QUANTIDADE_PRODUTO = """
    UPDATE item_pedido
    SET quantidade=quantidade+1
    WHERE id_pedido=? AND id_musica=?
"""

SQL_DIMINUIR_QUANTIDADE_PRODUTO = """
    UPDATE item_pedido
    SET quantidade=quantidade-1
    WHERE id_pedido=? AND id_musica=?
"""

SQL_EXCLUIR = """
    DELETE FROM item_pedido
    WHERE id_pedido=? AND id_musica=?
"""

SQL_OBTER_QUANTIDADE_POR_PEDIDO = """
    SELECT COUNT(*) FROM item_pedido
    WHERE id_pedido=?
"""
