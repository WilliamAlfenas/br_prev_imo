from enum import Enum
from typing import List

class Perfil(Enum):
    impulsivo = 0
    exigente = 1
    cauteloso = 2
    aleatorio = 3

class Jogador:
    def __init__(self, ordem_turno, perfil, saldo = 300, 
            pos_tabuleiro = 0, falido = False) :
        self.ordem_turno = ordem_turno
        self.perfil = perfil
        self.saldo = saldo
        self.pos_tabuleiro = pos_tabuleiro
        self.falido = falido

class Propriedade:
    def __init__(self, custo_venda, aluguel, proprietario = None):
        self.custo_venda = custo_venda
        self.aluguel = aluguel
        self.proprietario = proprietario

class Partida:
    def __init__(self, 
            tabuleiro: List[Propriedade], players: List[Jogador],
            perfil_vencedor = None, pos_turno = 0, qtd_rodadas = 0,
            qtd_falidos = 0):

        self.tabuleiro = tabuleiro
        self.players = players
        self.perfil_vencedor = perfil_vencedor
        self.pos_turno = pos_turno
        self.qtd_rodadas = qtd_rodadas
        self.qtd_falidos = qtd_falidos