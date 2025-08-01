from dataclasses import dataclass

@dataclass
class Peca:
    id: int
    nome: str
    codigo_oem: str
    descricao: str
    localizacao: str
    quantidade: int
    preco_custo: float
    preco_venda: float
    modelo_carro: str
    ano_carro: str

@dataclass
class Usuario:
    id: int
    username: str
    password_hash: str
    role: str
