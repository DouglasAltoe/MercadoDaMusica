SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS genero (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL)
"""

SQL_INSERIR = """
    INSERT INTO genero(descricao)
    VALUES (?)
"""

SQL_OBTER_TODOS = """
    SELECT id, descricao
    FROM genero
    ORDER BY descricao
"""

SQL_ALTERAR = """
    UPDATE genero
    SET descricao=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM genero    
    WHERE id=?
"""

SQL_OBTER_UM = """
    SELECT id, descricao
    FROM genero
    WHERE id=?
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) FROM genero
"""

SQL_OBTER_BUSCA = """
    SELECT id, descricao
    FROM genero
    WHERE descricao LIKE ?
    ORDER BY #1
    LIMIT ? OFFSET ?
"""

SQL_OBTER_QUANTIDADE_BUSCA = """
    SELECT COUNT(*) FROM genero
    WHERE descricao LIKE ?
"""