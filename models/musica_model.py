from dataclasses import dataclass
from typing import Optional


@dataclass
class Musica():
    id: Optional[int] = None
    nome: Optional[str] = None
    artista: Optional[str] = None
    preco: Optional[float] = None
    descricao: Optional[str] = None
    genero: Optional[int] = None