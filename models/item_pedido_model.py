from dataclasses import dataclass
from typing import Optional


@dataclass
class ItemPedido:
    id_pedido: Optional[int] = None
    id_musica: Optional[int] = None
    nome_musica: Optional[str] = None
    valor_musica: Optional[float] = None
    quantidade: Optional[int] = None
    valor_item: Optional[float] = None
