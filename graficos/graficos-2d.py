import matplotlib.pyplot as plt
import numpy as np


# Cria a figura e o eixo

# IMPORTANTE: figsize=(largura, altura) em Polegadas

# Gera pontos aleatórios
np.random.seed(42) # alimenta o gerador de números aleatórios com uma seed, permitindo que se gere o mesmo número aleatório a cada nova execução do programa.
n_pontos=100


x = np.linspace(0, 2*np.pi, n_pontos) # cria valores num espaço linear entre 0 e 2pi. A diferença entre números consecutidos é constante e dada por (stop-start)/(N-1)
y_base = np.random.rand(n_pontos) * 5 # Valores entre 0 e 5


# Coinfigura a figura e os eixos

## Nomeia a Janela dos gráficos
fig = plt.figure(figsize=(16, 9), num='Dashboard de Visualização') # Cria a figura com tamanho 16x9 polegadas e nomeia a janela

## Título geral da figura
fig.suptitle('Exemplos de Gráficos 2D com Matplotlib', fontsize=16) # Título geral da figura

## Ajusta o layout da figura
fig.tight_layout(pad=4.5) # Ajusta o layout para evitar sobreposição de elementos


# Cria uma grade de subplots nxn
axs = fig.subplots(2, 3) # Outra forma (2,3): ((ax1, ax2, ax3), (ax4, ax5, ax6)) 



# Plota de pontos no formato y = f(x)

## Senóide
axs[0,0].plot(x, np.sin(x),'o-', color='blue', alpha=0.6, markersize=2) # alpha é a transparência dos pontos (0-1)
axs[0,0].set_title('Gráfico de Linha com Marcadores: Senoidal', fontsize=11) # Título do gráfico
axs[0,0].set_xlabel('X') # Rótulo do eixo X
axs[0,0].set_ylabel('sin(X)') # Rótulo do eixo Y
axs[0,0].legend( labels=['y = sin(x)'], loc='upper right') # Adiciona legenda ao gráfico
axs[0,0].grid(True) # Adiciona uma grade ao gráfico

## Cossenóide
axs[0,1].plot(x, np.cos(x),'s--', color='green', alpha=0.6, markersize=2)
axs[0,1].set_title('Gráfico de Linha com Marcadores: Cossenoidal', fontsize=11)
axs[0,1].set_xlabel('X')
axs[0,1].set_ylabel('cos(X)')
axs[0,1].legend( labels=['y = cos(x)'], loc='upper center') # Adiciona legenda ao gráfico
axs[0,1].grid(True)

## Função Quadrática
axs[0,2].plot(x, x**2,'d-.', color='red', alpha=0.6, markersize=2)
axs[0,2].set_title('Gráfico de Linha com Marcadores: Quadrática', fontsize=11)
axs[0,2].set_xlabel('X')
axs[0,2].set_ylabel('X^2')
axs[0,2].legend( labels=['y = x^2'], loc='upper left') # Adiciona legenda ao gráfico
axs[0,2].grid(True)



# Gráfico Scatter

axs[1,0].scatter(x,y_base,color='red', alpha=0.6,s=10) # s é o tamanho dos pontos
axs[1,0].set_xlabel('X')
axs[1,0].set_ylabel('Y')
axs[1,0].set_title('Gráfico Scatter de Pontos Aleatórios', fontsize=11)
axs[1,0].grid(True)


# Gráfico com 3 séries lineares diferentes de y

for i in range(3):
     y = np.sin(x) * i + np.random.randn(n_pontos) * 0.5
     axs[1,1].plot(x, y, 'o-', label=f'Série {i+1}', alpha=0.7, markersize=2)

axs[1,1].set_xlabel('X')
axs[1,1].set_ylabel('Y')
axs[1,1].set_title('Múltiplas Séries Lineares de Dados Aleatórios', fontsize=11)
axs[1,1].legend()
axs[1,1].grid(True)


# Gera gráfico de Pizza
labels = ['A', 'B', 'C', 'D']
sizes = [15, 30, 45, 10]
colors = ['gold', 'lightgreen', 'lightcoral', 'lightskyblue']
explode = (0.2, 0, 0, 0)  # destaca o primeiro pedaço. Explore = n%, n%, n%, n% do raio (distância do centro)

axs[1,2].pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', 
        shadow={'ox': -0.02, 'edgecolor': 'none', 'shade': 0.5}, 
        startangle=90
        ) # configura o gráfico de pizza com porcentagens, sombra e ângulo inicial

axs[1,2].axis('equal')  # Garante que o gráfico de pizza seja um círculo
axs[1,2].set_title('Gráfico de Pizza', fontsize=11)
axs[1,2].legend(labels, loc='upper right')

# Mostra gráficos
plt.show()



