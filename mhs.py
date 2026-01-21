# Movimento Harmônico Simples (MHS)

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Definindo a EDO: y'' = -y  (transformada em sistema de 1ª ordem)
# Sendo y[0] = posição, y[1] = velocidade
def sistema(t, y):
    return [y[1], -y[0]]

# Resolver
sol = solve_ivp(sistema, [0, 20], [1, 0], t_eval=np.linspace(0, 20, 100))

# Plotar
plt.plot(sol.t, sol.y[0], label='Posição')
plt.plot(sol.t, sol.y[1], label='Velocidade')
plt.legend()
plt.show()