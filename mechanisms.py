from models import *
from typing import List
import random

QTD_PROPRIEDADES, QTD_JOGADORES = 20, 4
VLR_MIN_PROP, VLR_MAX_PROP = 50, 200
LIMIT_RODADAS, BONUS_VOLTA_TABULEIRO = 1000, 100
#Caculando o aluguel por 50% do valor do imóvel
CALC_ALUGUEL = lambda vlr_imovel: vlr_imovel >> 1

def cria_partida() -> Partida:
    return Partida(
        tabuleiro= [
            Propriedade(
                custo_venda = vlr_imovel,
                aluguel = CALC_ALUGUEL(vlr_imovel)
            )
            for vlr_imovel in (
                random.randint(VLR_MIN_PROP, VLR_MAX_PROP)
                for _ in range(QTD_PROPRIEDADES)
            )
        ],
        players = [
            Jogador(
                ordem_turno = i,
                perfil = Perfil(i)
            )
            for i in range(QTD_JOGADORES)
        ]
    )

def calc_partida() -> Partida:
    partida_atual = cria_partida()

    while(partida_atual.perfil_vencedor is None):
        partida_atual.qtd_rodadas += 1

        for turno in range(QTD_JOGADORES):
            partida_atual.pos_turno = turno
            player_atual = partida_atual.players[partida_atual.pos_turno]

            if player_atual.falido:
                continue
            
            calc_posicao_player(partida_atual)
            entrada_em_propriedade(partida_atual)

            if partida_atual.perfil_vencedor is not None:
                break

        if partida_atual.qtd_rodadas >= LIMIT_RODADAS:
            time_out(partida_atual)
    
    return partida_atual

def time_out(game: Partida):
    player_maior_saldo: Jogador = None

    for player in game.players:
        if player_maior_saldo is None \
                or player.saldo > player_maior_saldo.saldo:
            player_maior_saldo = player

    game.perfil_vencedor = player_maior_saldo.perfil

def calc_posicao_player(game: Partida):
    player = game.players[game.pos_turno]

    result_dado = random.randint(1, 6)
    player.pos_tabuleiro += result_dado

    if player.pos_tabuleiro >= QTD_PROPRIEDADES:
        player.saldo += BONUS_VOLTA_TABULEIRO
        player.pos_tabuleiro -= QTD_PROPRIEDADES

def entrada_em_propriedade(game: Partida):
    player = game.players[game.pos_turno]
    imovel = game.tabuleiro[player.pos_tabuleiro]

    if imovel.proprietario is None:
        return oportunidade_compra(imovel, player)
    
    if imovel.proprietario != player:
        player.saldo -= imovel.aluguel
        imovel.proprietario.saldo += imovel.aluguel

        if player.saldo < 0:
            saldo_negativo(player, game)

def oportunidade_compra(imovel: Propriedade, player: Jogador):
    funs_decisao = {
        'impulsivo': lambda: imovel.custo_venda <= player.saldo,
        'exigente': lambda: imovel.aluguel > 50,
        'cauteloso': lambda: player.saldo - imovel.custo_venda > 80,
        'aleatorio': lambda: random.randint(0, 1) == 1
    }

    if funs_decisao[player.perfil.name]() == True:
        imovel.proprietario = player
        player.saldo -= imovel.custo_venda

def saldo_negativo(player: Jogador, game: Partida):
    for imovel in game.tabuleiro:
        if imovel.proprietario == player:
            imovel.proprietario = None
    
    player.falido = True
    game.qtd_falidos += 1

    if game.qtd_falidos >= QTD_JOGADORES - 1:
        last_active_player(game)

def last_active_player(game: Partida):
    for player in game.players:
        if not player.falido:
            game.perfil_vencedor = player.perfil
            break