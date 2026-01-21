import numpy as np
from ursina import *
from ursina.shaders import unlit_shader


# --- 1. MOTOR FÍSICO (O mesmo de antes) ---
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
        campo_freq = amplitude * np.exp(1j * fase)
        self.psi = np.real(np.fft.ifft2(campo_freq))
        self.psi = (self.psi - self.psi.mean()) / self.psi.std()
        v_y, v_x = np.gradient(self.psi)
        self.u = -v_y * 100.0  # Velocidade ajustada para escala do Ursina
        self.v = v_x * 100.0

    def get_velocity_at(self, x, y, scale_factor):
        # Mapeamento com proteção de limites (Wrap around)
        norm_x = (x / scale_factor * self.N).astype(int) % self.N
        norm_y = (y / scale_factor * self.N).astype(int) % self.N
        return self.u[norm_y, norm_x], self.v[norm_y, norm_x], self.psi[norm_y, norm_x]


# --- 2. CONFIGURAÇÃO URSINA ---
app = Ursina()

# Configuração da Janela e Câmera
window.color = color.black
window.title = "Ursina Turbulence - Neon Edition"
camera.position = (0, -20, -60)
camera.rotation_x = -30

# Parâmetros
NUM_PARTICLES = 10000
WORLD_SIZE = 50

# Inicializar Física
motor = KolmogorovField(N=256)

# Posições Iniciais (Array NumPy para velocidade)
positions = (np.random.rand(NUM_PARTICLES, 3) - 0.5) * WORLD_SIZE
positions[:, 2] = 0  # Z é altura

# --- 3. CRIAÇÃO DA MALHA (O Segredo da Performance) ---
# Em vez de 10k objetos, criamos 1 objeto com 10k vértices
cloud = Entity(
    model=Mesh(vertices=positions, mode="point", static=False),
    color=color.cyan,
    scale=1,
)

# Hack visual: Pontos no Ursina podem ser pequenos demais.
# Às vezes usamos 'line_strip' ou shaders customizados, mas 'point' é o mais rápido.

# --- 4. EFEITOS VISUAIS (A Vantagem do Ursina) ---
from ursina.prefabs.first_person_controller import FirstPersonController

# EditorCamera() # Descomente para controlar com mouse livremente
# BLOOM: O efeito "Neon" que faz as partículas brilharem
from ursina.shaders import camera_grayscale_shader

camera.shader = None  # Reset
bloom = BloomEffect()
bloom.threshold = 0.5  # Só brilha o que for bem claro
bloom.blur = 10


# --- 5. GAME LOOP ---
def update():
    global positions

    # 1. Obter velocidades
    # Nota: Ursina usa eixos X, Y, Z. Aqui mapearemos Y do 2D para Z do 3D ou Y do 3D.
    # Vamos assumir plano X/Y e Z é altura.
    u, v, h = motor.get_velocity_at(
        positions[:, 0] + WORLD_SIZE / 2, positions[:, 1] + WORLD_SIZE / 2, WORLD_SIZE
    )

    # 2. Atualizar Posições (Euler Integration)
    dt = time.dt * 0.5
    positions[:, 0] += u * dt
    positions[:, 1] += v * dt

    # Altura baseada no Psi (Relevo)
    positions[:, 2] = h * 2.0

    # 3. Teleporte nas bordas (Wrap)
    # Lógica NumPy rápida para manter dentro do cubo
    half = WORLD_SIZE / 2
    positions[:, 0] = ((positions[:, 0] + half) % WORLD_SIZE) - half
    positions[:, 1] = ((positions[:, 1] + half) % WORLD_SIZE) - half

    # 4. Atualizar a Malha na GPU
    # Esta linha envia os novos vértices para a placa de vídeo
    cloud.model.vertices = positions
    cloud.model.generate()


# Texto de Info
Text(
    text="Ursina Engine: Mesh Points + Bloom",
    position=(-0.85, 0.45),
    scale=1.5,
    color=color.cyan,
)

app.run()
