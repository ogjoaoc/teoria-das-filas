import simpy
import random
import numpy as np

#Macros e constantes
TAXA_CHEGADA = 0.5
TAXA_SERVICO = 1.0
NUM_SERVIDORES = 1
TEMPO_SIMULACAO = 10000

tempo_de_espera = []

#Função de solicitação de chegada
def cliente(env, nome, servidor):
  chegada = env.now

  print(f'{nome} chegou em {chegada:.2f}')

  with servidor.request() as req:
    yield req
    inicio_servico = env.now

    tempo_de_espera.append(inicio_servico - chegada)

    print(f'{nome} começou o atendimento em {inicio_servico:.2f}')

    tempo_atendimento = random.expovariate(TAXA_SERVICO)
    yield env.timeout(tempo_atendimento)

    fim_servico = env.now
    print(f'{nome} terminou o atendimento em {fim_servico:.2f}')


#Gera as chegadas dos clientes
def gerar_clientes(env, servidor):
  contador = 0
  while 1:
    yield env.timeout(random.expovariate(TAXA_CHEGADA))
    contador += 1
    env.process(cliente(env, f'Cliente {contador}', servidor))

def simular():
  env = simpy.Environment()
  servidor = simpy.Resource(env, capacity=NUM_SERVIDORES)
  env.process(gerar_clientes(env, servidor))
  env.run(until=TEMPO_SIMULACAO)

  print(f'Tempo médio de espera (W) : {np.mean(tempo_de_espera)}')
  print(f'Variância do tempo médio de espera (W) : {np.var(tempo_de_espera)}')

simular()

