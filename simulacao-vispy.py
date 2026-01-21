import sys

import numpy as np
from vispy import app, scene

# --- 1. CONFIGURAÇÕES ---
NUM_PARTICLES = 50000  # Pygame engasga com 10k, VisPy ri com 50k
WIDTH_MAP = 100  # Tamanho do mundo físico


# --- 2. O MOTOR FÍSICO (O mesmo do original, estático) ---
class KolmogorovField:
    def __init__(self, N=256, slope=2.0):
        self.N = N
        kx = np.fft.fftfreq(N)
        ky = np.fft.fftfreq(N)
        kx_grid, ky_grid = np.meshgrid(kx, ky)
        k = np.sqrt(kx_grid**2 + ky_grid**2)
        k[0, 0] = 1.0
        amplitude = k ** (-slope / 2.0)
        amplitude[0, 0] = 0
        fase = 2 * np.pi * np.random.rand(N, N)

        # Gerar campo
        campo_freq = amplitude * np.exp(1j * fase)
        self.psi = np.real(np.fft.ifft2(campo_freq))
        self.psi = (self.psi - self.psi.mean()) / self.psi.std()

        # Calcular velocidades (Derivadas)
        v_y, v_x = np.gradient(self.psi)
        self.u = -v_y * 2.0  # Fator de velocidade
        self.v = v_x * 2.0

    def get_velocity_at(self, x, y):
        # Mapear coordenadas do mundo (0 a 100) para indices da matriz (0 a 256)
        # Usamos interpolação "vizinho mais próximo" para performance máxima
        idx_x = (x / WIDTH_MAP * self.N).astype(int) % self.N
        idx_y = (y / WIDTH_MAP * self.N).astype(int) % self.N

        return self.u[idx_y, idx_x], self.v[idx_y, idx_x], self.psi[idx_y, idx_x]


# --- 3. CONFIGURAÇÃO VISPY ---
canvas = scene.SceneCanvas(
    keys="interactive", title="Partículas Lagrangianas (GPU)", show=True
)
view = canvas.central_widget.add_view()
view.camera = "turntable"
view.camera.distance = 150
view.camera.elevation = 30

# Inicializar Física
motor = KolmogorovField(N=512, slope=2.0)

# Criar Partículas Iniciais
# pos[:, 0] = x, pos[:, 1] = y, pos[:, 2] = z (altura)
pos = np.random.rand(NUM_PARTICLES, 3) * WIDTH_MAP
pos[:, 2] = 0  # Começam no chão

# Criar o Visual de Pontos (Markers)
# scatter é muito otimizado para desenhar milhares de pontos iguais
scatter = scene.visuals.Markers(parent=view.scene)

# Estética: Pontos pequenos, translúcidos, cor ciano/azul
scatter.set_data(pos, edge_color=None, face_color=(0, 1, 1, 0.5), size=2)

# Eixos para referência
axis = scene.visuals.XYZAxis(parent=view.scene)


# --- 4. GAME LOOP (Atualização de Partículas) ---
def update(event):
    global pos

    # 1. Obter velocidade baseada na posição atual (X, Y)
    u, v, altura_psi = motor.get_velocity_at(pos[:, 0], pos[:, 1])

    # 2. Mover partículas (Advecção)
    pos[:, 0] += u * 0.5  # dt
    pos[:, 1] += v * 0.5

    # 3. Atualizar altura (Z) para elas surfarem a topologia
    # Multiplico por 10 para exagerar o relevo
    pos[:, 2] = altura_psi * 5.0

    # 4. Wrap-around (Toroidal) - Se sair do mapa, volta do outro lado
    pos[:, 0] = pos[:, 0] % WIDTH_MAP
    pos[:, 1] = pos[:, 1] % WIDTH_MAP

    # 5. Enviar novos dados para a GPU
    scatter.set_data(pos, edge_color=None, face_color=(0, 1, 1, 0.6), size=3)

    canvas.update()


timer = app.Timer(interval=0, connect=update, start=True)  # interval=0 = Max FPS

if __name__ == "__main__":
    if sys.flags.interactive != 1:
        app.run()
