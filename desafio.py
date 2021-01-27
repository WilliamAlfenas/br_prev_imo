from mechanisms import calc_partida, QTD_JOGADORES, LIMIT_RODADAS
from models import Partida, Perfil
from tqdm import tqdm #pip install tqdm

QTD_SIMULACOES = 300

qtd_timeouts, tot_turnos = 0, 0
qtd_vitorias = {
    Perfil(i).name: 0
    for i in range(QTD_JOGADORES)
}

print(f'''
--------------Seja Bem Vindo a minha Resposta de Desafio--------------

Agora estarei rodando {QTD_SIMULACOES} simulações conforme solicitado.

Por favor, aguarde.
''')

for _ in tqdm(range(QTD_SIMULACOES)):
    result = calc_partida()

    if result.qtd_rodadas >= LIMIT_RODADAS:
        qtd_timeouts += 1

    qtd_vitorias[result.perfil_vencedor.name] += 1
    tot_turnos += result.qtd_rodadas

print(f'''
------------------------Resultados------------------------

+Quantidade de partidas terminadas por Time out 
 --{qtd_timeouts}/{QTD_SIMULACOES} partidas
+Média de turnos entre as partidas
 --{tot_turnos/QTD_SIMULACOES:0.2f} turnos''')

maior_qtd_vit, perfil_vencedor = 0, ''
for perfil, tot_vit in qtd_vitorias.items():
    print(f'+Percentual de vitórias do {perfil}\n',
    f'--{tot_vit*100/QTD_SIMULACOES:0.2f}%')

    if tot_vit > maior_qtd_vit:
        maior_qtd_vit = tot_vit
        perfil_vencedor = perfil

print(f'+O perfil mais vitorioso é por tanto:\n',
    f'--{perfil_vencedor} com {maior_qtd_vit}/{QTD_SIMULACOES} vitórias')