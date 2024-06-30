SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS musica (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        artista TEXT NOT NULL,
        preco FLOAT NOT NULL,
        descricao TEXT NOT NULL,
        genero INTEGER NOT NULL,
        FOREIGN KEY (genero) REFERENCES genero(id))
"""

SQL_INSERIR = """
    INSERT INTO musica(nome, artista, preco, descricao, genero)
    VALUES (?, ?, ?, ?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT id, nome, artista, preco, descricao, genero
    FROM musica
    ORDER BY nome
"""

SQL_ALTERAR = """
    UPDATE musica
    SET nome=?, preco=?, artista=?, descricao=?, genero=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM musica    
    WHERE id=?
"""

SQL_OBTER_UM = """
    SELECT id, nome, artista, preco, descricao, genero
    FROM musica
    WHERE id=?
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) FROM musica
"""

SQL_OBTER_BUSCA = """
    SELECT id, nome, artista, preco, descricao, genero
    FROM musica
    WHERE nome LIKE ? OR descricao LIKE ?
    ORDER BY #1
    LIMIT ? OFFSET ?
"""

SQL_OBTER_QUANTIDADE_BUSCA = """
    SELECT COUNT(*) FROM musica
    WHERE nome LIKE ? OR descricao LIKE ?
"""