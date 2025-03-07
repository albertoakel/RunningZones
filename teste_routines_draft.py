import matplotlib.pyplot as plt
import numpy as np

# Dados de exemplo
x = np.linspace(0, 10, 100)
dado1 = np.sin(x)
dado2 = np.cos(x)
dado3 = np.sin(x) * np.cos(x)

# Criando a figura e o eixo
fig, ax = plt.subplots()
for i in range(3):
    ax.clear()  # Limpa o eixo para o próximo gráfico
    dado=(1+x**i)*np.sin(x)
    ax.plot(x, dado)  # Plota os dados
    ax.legend()  # Adiciona a legenda
    plt.draw()  # Atualiza o gráfico
    plt.pause(0.1)  # Pausa para garantir que o gráfico seja exibido
    plt.waitforbuttonpress()