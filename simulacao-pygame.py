import os
from datetime import datetime
from typing import List, Optional, Tuple

import matplotlib

matplotlib.use("TkAgg")

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pygame

agora: datetime = datetime.now()
timestamp: str = agora.strftime("%Y%m%d_%H%M")

VIDEO_FILE_NAME: str = f"simulacao-{timestamp}.mp4"
CAPTURAS_PATH: str = "capturas"


def criar_video(pasta_origem: str, nome_video_saida: str, fps: int = 30) -> None:
    """
    Cria um vídeo a partir de uma sequência de imagens PNG.

    Args:
        pasta_origem: Caminho da pasta contendo as imagens
        nome_video_saida: Nome do arquivo de vídeo de saída
        fps: Taxa de quadros por segundo
    """
    image_folder: str = pasta_origem
    video_name: str = nome_video_saida

    # Filtrar apenas arquivos PNG
    images: List[str] = [
        img for img in os.listdir(image_folder) if img.endswith(".png")
    ]
    images.sort()

    if not images:
        print(f"Nenhuma imagem encontrada em {image_folder}")
        return

    # Obter dimensões do primeiro frame
    first_image_path: str = os.path.join(image_folder, images[0])
    frame: np.ndarray = cv2.imread(first_image_path)

    if frame is None:
        print(f"Erro ao ler a imagem {first_image_path}")
        return

    height: int
    width: int
    layers: int
    height, width, layers = frame.shape

    # Configurar codec de vídeo
    fourcc: int = cv2.VideoWriter_fourcc(*"mp4v")
    video: cv2.VideoWriter = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    print(f"Gerando vídeo '{video_name}' com {len(images)} frames...")

    # Processar cada imagem
    for image in images:
        image_path: str = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)
        if frame is not None:
            video.write(frame)
        else:
            print(f"Aviso: Não foi possível ler {image_path}")

    cv2.destroyAllWindows()
    video.release()
    print("Vídeo concluído com sucesso!")


# MOTOR DE FÍSICA (Compartilhado)
class KolmogorovField:
    """Simula um campo de turbulência baseado na teoria de Kolmogorov."""

    def __init__(self, N: int = 512, slope: float = 2.0) -> None:
        """
        Inicializa o campo de Kolmogorov.

        Args:
            N: Tamanho da grade (N x N)
            slope: Declive do espectro de energia
        """
        self.N: int = N
        self.slope: float = slope

        # Configurar grade de frequência
        kx: np.ndarray = np.fft.fftfreq(N)
        ky: np.ndarray = np.fft.fftfreq(N)
        kx_grid: np.ndarray
        ky_grid: np.ndarray
        kx_grid, ky_grid = np.meshgrid(kx, ky)

        k: np.ndarray = np.sqrt(kx_grid**2 + ky_grid**2)
        k[0, 0] = 1.0

        # Amplitude fixa baseada na lei de potência
        self.amplitude: np.ndarray = k ** (-slope / 2.0)
        self.amplitude[0, 0] = 0

        # Estado inicial (fase aleatória)
        self.fase: np.ndarray = 2 * np.pi * np.random.rand(N, N)

    def get_velocity_field(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Retorna os vetores de velocidade U e V do campo atual.

        Returns:
            Tuple contendo:
            - u: Componente x da velocidade
            - v: Componente y da velocidade
            - psi: Função de corrente
        """
        # Gerar campo complexo
        campo_freq: np.ndarray = self.amplitude * np.exp(1j * self.fase)
        psi: np.ndarray = np.real(np.fft.ifft2(campo_freq))

        # Normalizar função de corrente
        psi = (psi - psi.mean()) / psi.std()

        # Calcular velocidades (Rotacional)
        v_y: np.ndarray
        v_x: np.ndarray
        v_y, v_x = np.gradient(psi)

        # Fator de escala para velocidade visual
        ESCALA_VELOCIDADE: float = 50.0
        u: np.ndarray = -v_y * ESCALA_VELOCIDADE
        v: np.ndarray = v_x * ESCALA_VELOCIDADE

        return u, v, psi

    def get_spectrum(self, psi: np.ndarray) -> np.ndarray:
        """
        Calcula o espectro de energia radial.

        Args:
            psi: Função de corrente

        Returns:
            Perfil radial do espectro de energia
        """
        fourier: np.ndarray = np.fft.fftshift(np.fft.fft2(psi))
        psd: np.ndarray = np.abs(fourier) ** 2

        y: np.ndarray
        x: np.ndarray
        y, x = np.indices((self.N, self.N))
        center: np.ndarray = np.array([self.N // 2, self.N // 2])
        r: np.ndarray = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2).astype(int)

        tbin: np.ndarray = np.bincount(r.ravel(), psd.ravel())
        nr: np.ndarray = np.bincount(r.ravel())
        radial_profile: np.ndarray = tbin / np.maximum(nr, 1)

        return radial_profile


# A PROVA CIENTÍFICA
def mostrar_grafico_estatico(motor: KolmogorovField) -> None:
    """
    Gera e salva um gráfico estático do espectro de energia.

    Args:
        motor: Instância do campo de Kolmogorov
    """
    print("Gerando gráfico de análise e salvando como 'espectro_kolmogorov.png'...")

    u: np.ndarray
    v: np.ndarray
    psi: np.ndarray
    u, v, psi = motor.get_velocity_field()

    spectrum: np.ndarray = motor.get_spectrum(psi)
    k_axis: np.ndarray = np.arange(len(spectrum))

    plt.figure(figsize=(8, 6))
    start: int = 5
    end: int = 100

    # Plotar dados da simulação
    plt.loglog(k_axis[start:end], spectrum[start:end], "c-", lw=2, label="Simulação")

    # Plotar curva teórica
    teoria: np.ndarray = k_axis[start:end] ** -2.6  # Slope ajustado
    scale: float = spectrum[start] / teoria[0]
    plt.loglog(k_axis[start:end], teoria * scale, "r--", label="Teoria de Kolmogorov")

    plt.title("Validação Matemática: Espectro de Energia")
    plt.xlabel("Frequência Espacial (k)")
    plt.ylabel("Energia E(k)")
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)

    # Salvar gráfico
    plt.savefig("espectro_kolmogorov.png", dpi=150, bbox_inches="tight")
    print("Gráfico salvo! Iniciando simulação visual...")
    plt.close()  # Fecha a figura para liberar memória


# A SIMULAÇÃO VISUAL
def rodar_simulacao_pygame(motor: KolmogorovField) -> None:
    """
    Executa a simulação visual interativa usando PyGame.

    Args:
        motor: Instância do campo de Kolmogorov
    """
    # Configurações da simulação
    WIDTH: int = 800
    HEIGHT: int = 800
    NUM_PARTICLES: int = 10000
    BACKGROUND_COLOR: Tuple[int, int, int] = (5, 5, 20)  # Azul noturno profundo
    FPS: int = 60

    # Paleta Van Gogh (Azul -> Ciano -> Amarelo)
    COLORS: List[Tuple[int, int, int]] = [
        (28, 63, 117),  # Azul Médio
        (86, 152, 196),  # Ciano
        (232, 216, 74),  # Amarelo Ouro
    ]

    # Inicializar PyGame
    _ = pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Turbulências de Van Gogh - Simulação usando Kolmogorov")
    clock: pygame.time.Clock = pygame.time.Clock()

    # Gerar campo de velocidade inicial
    print("Calculando campo de vetores...")
    u_grid: np.ndarray
    v_grid: np.ndarray
    psi: np.ndarray
    u_grid, v_grid, _ = motor.get_velocity_field()

    # Criar partículas (posições aleatórias)
    particles: np.ndarray = np.random.rand(NUM_PARTICLES, 2) * [WIDTH, HEIGHT]

    # Estado da simulação
    pausado: bool = False
    gravado: bool = False
    contador_frames: int = 0
    nome_pasta: str = "capturas"
    running: bool = True

    # Criar pasta para capturas se não existir
    if not os.path.exists(nome_pasta):
        os.makedirs(nome_pasta)

    # Configurar fonte para UI
    pygame.font.init()
    fonte_ui: pygame.font.Font = pygame.font.SysFont("Arial", 24)

    while running:
        # Processar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    pausado = not pausado
                elif event.key == pygame.K_s:
                    gravado = not gravado
                    if gravado:
                        print("Gravação iniciada...")
                    else:
                        print("Gravação finalizada.")
                        print("Criando arquivo de vídeo da simulação...")
                        criar_video(CAPTURAS_PATH, VIDEO_FILE_NAME, fps=FPS)

        if not pausado:
            # Lógica de Física (Lagrangiana)
            # 1. Mapear posições das partículas para a grade
            grid_x: np.ndarray = (particles[:, 0] / WIDTH * motor.N).astype(
                int
            ) % motor.N
            grid_y: np.ndarray = (particles[:, 1] / HEIGHT * motor.N).astype(
                int
            ) % motor.N

            # 2. Obter velocidade na célula correspondente
            p_u: np.ndarray = u_grid[grid_y, grid_x]
            p_v: np.ndarray = v_grid[grid_y, grid_x]

            # 3. Mover partículas
            DT: float = 0.1  # Passo de tempo
            particles[:, 0] += p_u * DT
            particles[:, 1] += p_v * DT

            # 4. Wrap-around (espaço toroidal)
            particles[:, 0] = particles[:, 0] % WIDTH
            particles[:, 1] = particles[:, 1] % HEIGHT

            # --- Renderização ---
            # Efeito de rastro (trail)
            fade_surface: pygame.Surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.set_alpha(20)  # Transparência
            _ = fade_surface.fill(BACKGROUND_COLOR)
            _ = screen.blit(fade_surface, (0, 0))

            # Desenhar partículas baseadas na velocidade
            speeds: np.ndarray = np.sqrt(p_u**2 + p_v**2)
            max_speed: float = np.percentile(
                speeds, 95
            )  # Normalizar ignorando outliers

            # Acesso direto aos pixels para melhor performance
            pixel_array: np.ndarray = pygame.surfarray.pixels3d(screen)

            # Colorir partículas baseado na velocidade
            for i in range(NUM_PARTICLES):
                x: int = int(particles[i, 0])
                y: int = int(particles[i, 1])
                speed_ratio: float = min(speeds[i] / max_speed, 1.0)

                # Escolher cor baseada na velocidade
                if speed_ratio > 0.6:
                    color: Tuple[int, int, int] = COLORS[2]  # Amarelo
                elif speed_ratio > 0.3:
                    color = COLORS[1]  # Ciano
                else:
                    color = COLORS[0]  # Azul

                # Desenhar (com verificação de limites)
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    pixel_array[x, y] = color

            del pixel_array  # Liberar trava da superfície

        # Indicador de pausa
        if pausado:
            texto_pausa: pygame.Surface = fonte_ui.render("PAUSADO", True, (255, 0, 0))
            _ = screen.blit(texto_pausa, (10, 10))

        # Indicador de gravação
        if gravado:
            _ = pygame.draw.circle(screen, (255, 0, 0), (WIDTH - 20, 20), 10)

            # Salvar frame atual
            nome_arquivo: str = f"{nome_pasta}/img_{contador_frames:05d}.png"
            pygame.image.save(screen, nome_arquivo)
            contador_frames += 1

        pygame.display.flip()
        _ = clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    # 1. Configurar Física
    motor_fisico: KolmogorovField = KolmogorovField(N=512, slope=2.0)

    # 2. Mostrar Análise Matemática
    mostrar_grafico_estatico(motor_fisico)

    # 3. Iniciar Simulação Interativa
    rodar_simulacao_pygame(motor_fisico)
