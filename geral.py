import random
import math
import matplotlib
import numpy
import FreeSimpleGUI
 

# Constantes de Eventos
EVENTO_CHEGADA = "CHEGADA"
EVENTO_SAIDA = "SAIDA"
def gera_intervalo_chegada(taxa_chegada_hora):
"""Gera intervalo entre chegadas (em minutos) com base num Processo de 
Poisson."""
taxa_minuto = taxa_chegada_hora / 60.0
u = random.random()
return -math.log(1.0 - u) / taxa_minuto
def gera_tempo_servico(tipo_distrib, media, desvio=1.5):
"""Gera a duração do processamento (em minutos) garantindo valor 
positivo."""
if tipo_distrib == "exponential":
return random.expovariate(1.0 / media)
elif tipo_distrib == "uniform":
return random.uniform(max(1.0, media - 3.0), media + 3.0)
elif tipo_distrib == "normal":
return max(1.0, random.gauss(media, desvio))
return media
def simula_laboratorio(config):
tempo_atual = 0.0
contador_amostras = 0
amostras_concluidas = 0
# Lista de eventos futuros ordenada por tempo: [(tempo, tipo_evento, 
id_amostra, ...)]
4 / 8
    lista_eventos = []
    
    # Fila de espera de amostras: armazena dicionários ou tuplos 
(id_amostra, tempo_chegada)
    fila_espera = []
    
    # Inicialização das máquinas com dicionários
    maquinas = [
        {
            "id": f"MQ_{i+1}",
            "ocupada": False,
            "amostra_atual": None,
            "inicio_ocupacao": 0.0,
            "tempo_total_trabalho": 0.0,
            "total_processadas": 0
        }
        for i in range(config["num_maquinas"])
    ]
    
    # Agendamento da primeira chegada
    contador_amostras += 1
    t_primeira = gera_intervalo_chegada(config["lambda_rate"])
    lista_eventos.append((t_primeira, EVENTO_CHEGADA, 
f"A_{contador_amostras}"))
    
    # Loop principal da simulação
    while lista_eventos:
        # Ordenar e retirar o evento cronologicamente mais próximo
        lista_eventos.sort(key=lambda ev: ev[0])
        evento_atual = lista_eventos.pop(0)
        tempo_atual = evento_atual[0]
        tipo_evento = evento_atual[1]
        id_amostra = evento_atual[2]
        
        if tipo_evento == EVENTO_CHEGADA:
            # 1. Agendar a próxima chegada se ainda estiver dentro do 
horário
            prox_t = tempo_atual + 
gera_intervalo_chegada(config["lambda_rate"])
            if prox_t <= config["simulation_time"]:
                contador_amostras += 1
                lista_eventos.append((prox_t, EVENTO_CHEGADA, 
f"A_{contador_amostras}"))
                
            # 2. Procurar máquina livre
            maquina_livre = next((m for m in maquinas if not m["ocupada"]), 
None)
            
            if maquina_livre:
                # Ocupar máquina imediatamente
                maquina_livre["ocupada"] = True
                maquina_livre["amostra_atual"] = id_amostra
                maquina_livre["inicio_ocupacao"] = tempo_atual
                
projeto-laboratorio.md 2026-11-02
5 / 8
projeto-laboratorio.md
2026-11-02
duracao = 
gera_tempo_servico(config["service_distribution"], 
config["mean_service_time"])
lista_eventos.append((tempo_atual + duracao, EVENTO_SAIDA, 
id_amostra, maquina_livre["id"]))
else:
# Enviar amostra para a fila com carimbo de tempo de 
chegada
fila_espera.append({"id": id_amostra, "tempo_chegada": 
tempo_atual})
elif tipo_evento == EVENTO_SAIDA:
id_maquina = evento_atual[3]
maq = next(m for m in maquinas if m["id"] == id_maquina)
# Atualizar estatísticas da máquina
tempo_trabalho = tempo_atual - maq["inicio_ocupacao"]
maq["tempo_total_trabalho"] += tempo_trabalho
maq["total_processadas"] += 1
amostras_concluidas += 1
# Verificar se há amostras a aguardar na fila
if fila_espera:
proxima = fila_espera.pop(0)
maq["amostra_atual"] = proxima["id"]
maq["inicio_ocupacao"] = tempo_atual
duracao = 
gera_tempo_servico(config["service_distribution"], 
config["mean_service_time"])
lista_eventos.append((tempo_atual + duracao, EVENTO_SAIDA, 
proxima["id"], maq["id"]))
else:
maq["ocupada"] = False
maq["amostra_atual"] = None
return {
"amostras_concluidas": amostras_concluidas,
"maquinas": maquinas,
"tempo_final": tempo_atual
}