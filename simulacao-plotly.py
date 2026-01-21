import numpy as np
import plotly.graph_objects as go


# --- 1. MOTOR FÍSICO COM TEMPO (t) ---
class TimeVaryingKolmogorov:
    def __init__(self, N=100, slope=3.0):
        # N reduzido para 100 para garantir fluidez na animação do navegador
        self.N = N

        # Configurar grade de frequência
        kx = np.fft.fftfreq(N)
        ky = np.fft.fftfreq(N)
        kx_grid, ky_grid = np.meshgrid(kx, ky)
        self.k = np.sqrt(kx_grid**2 + ky_grid**2)
        self.k[0, 0] = 1.0

        # Amplitude fixa (Lei de Potência)
        self.amplitude = self.k ** (-slope / 2.0)
        self.amplitude[0, 0] = 0

        # Estado inicial da fase (Semente)
        self.fase_base = 2 * np.pi * np.random.rand(N, N)

        # Frequência de oscilação temporal (para as ondas se mexerem)
        # Ondas maiores movem-se mais devagar, ondas menores mais rápido (Dispersão)
        self.omega = np.sqrt(self.k) * 1.0

    def get_psi_at_time(self, t):
        """Calcula o campo Psi no instante t"""
        # A fase evolui linearmente com o tempo: Fase = Fase_Inicial + Omega * t
        fase_atual = self.fase_base + self.omega * t

        campo_freq = self.amplitude * np.exp(1j * fase_atual)
        psi = np.real(np.fft.ifft2(campo_freq))

        # Normalização visual
        psi = (psi - psi.mean()) / psi.std()
        return psi


# --- 2. GERAÇÃO DA ANIMAÇÃO PLOTLY ---
def criar_animacao_turbulencia():
    print("Inicializando física...")
    N = 100
    motor = TimeVaryingKolmogorov(N=N, slope=3.0)

    # Grid espacial para o plot
    x = np.linspace(0, 10, N)
    y = np.linspace(0, 10, N)

    # Configurações da Animação
    total_frames = 150
    dt = 0.1  # Passo de tempo

    print(
        f"Calculando {total_frames} quadros de simulação (pode levar alguns segundos)..."
    )

    # 1. Gerar Dados Iniciais
    z_inicial = motor.get_psi_at_time(0)

    # 2. Criar Figura Base
    fig = go.Figure(
        data=[
            go.Surface(
                z=z_inicial,
                x=x,
                y=y,
                colorscale="Viridis",  # Escala clássica científica
                cmin=-3,
                cmax=3,  # Travar a escala de cor para não piscar
                contours_z=dict(show=True, usecolormap=True, project_z=True),
            )
        ]
    )

    # 3. Gerar Frames (Pré-renderização)
    frames = []
    for i in range(total_frames):
        t = i * dt
        z_t = motor.get_psi_at_time(t)

        frames.append(
            go.Frame(
                data=[go.Surface(z=z_t)],
                name=str(i),  # Identificador do frame
            )
        )

    print("Montando layout e controles...")

    # 4. Configurar Layout e Botões de Play
    fig.update_layout(
        title="Evolução Temporal do Campo de Kolmogorov",
        width=1000,
        height=800,
        scene=dict(
            zaxis=dict(range=[-4, 4], title="Psi"),  # Travar eixo Z
            aspectratio=dict(x=1, y=1, z=0.4),
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.4)),
        ),
        # Menus de Controle (Play/Pause)
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [
                            None,
                            {
                                "frame": {"duration": 50, "redraw": True},
                                "fromcurrent": True,
                            },
                        ],
                        "label": "Play",
                        "method": "animate",
                    },
                    {
                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": True},
                                "mode": "immediate",
                                "transition": {"duration": 0},
                            },
                        ],
                        "label": "Pause",
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top",
            }
        ],
        # Barra de Progresso (Slider)
        sliders=[
            {
                "active": 0,
                "yanchor": "top",
                "xanchor": "left",
                "currentvalue": {
                    "font": {"size": 20},
                    "prefix": "Tempo: ",
                    "visible": True,
                    "xanchor": "right",
                },
                "transition": {"duration": 50, "easing": "cubic-in-out"},
                "pad": {"b": 10, "t": 50},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [
                            [f.name],
                            {
                                "frame": {"duration": 50, "redraw": True},
                                "mode": "immediate",
                            },
                        ],
                        "label": str(k),
                        "method": "animate",
                    }
                    for k, f in enumerate(frames)
                ],
            }
        ],
        template="plotly_dark",
    )

    # Injetar os frames na figura
    fig.frames = frames

    fig.show()


if __name__ == "__main__":
    criar_animacao_turbulencia()
