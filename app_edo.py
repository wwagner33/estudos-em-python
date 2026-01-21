import tkinter as tk
from tkinter import ttk
import sympy as sp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class EDOStudyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Estudo de EDOs com SymPy")
        self.root.geometry("900x700")

        # Configuração do Layout Principal
        # Esquerda: Botões | Direita: Código e Resultado
        left_frame = ttk.Frame(root, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        right_frame = ttk.Frame(root, padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Painel Esquerdo (Controles) ---
        ttk.Label(left_frame, text="Exemplos do Livro", font=("Arial", 12, "bold")).pack(pady=10)
        
        ttk.Button(left_frame, text="1. Oscilador Harmônico (Geral)", 
                   command=self.exemplo_oscilador_geral).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="2. Oscilador com PVI", 
                   command=self.exemplo_oscilador_pvi).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="3. Equação da Capa (4ª Ordem)", 
                   command=self.exemplo_capa_livro).pack(fill=tk.X, pady=5)
        
        ttk.Separator(left_frame, orient='horizontal').pack(fill='x', pady=20)
        ttk.Button(left_frame, text="Sair", command=root.quit).pack(fill=tk.X, pady=5)

        # --- Painel Direito (Visualização) ---
        
        # 1. Área de Código (Texto)
        ttk.Label(right_frame, text="Código SymPy:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.text_code = tk.Text(right_frame, height=12, bg="#f0f0f0", font=("Consolas", 10))
        self.text_code.pack(fill=tk.X, pady=(0, 20))

        # 2. Área de Resultado (Matplotlib Canvas para renderizar LaTeX)
        ttk.Label(right_frame, text="Solução Matemática:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('off') # Desliga eixos X e Y
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def mostrar_resultado(self, codigo_str, latex_str):
        """Atualiza a interface com o código e a equação renderizada"""
        # Atualizar código
        self.text_code.delete(1.0, tk.END)
        self.text_code.insert(tk.END, codigo_str)
        
        # Atualizar gráfico (Renderizar LaTeX)
        self.ax.clear()
        self.ax.axis('off')
        
        # O $...$ diz ao Matplotlib para usar modo matemático
        texto_latex = f"${latex_str}$"
        
        # Desenha o texto no centro da figura
        self.ax.text(0.5, 0.5, texto_latex, fontsize=16, ha='center', va='center')
        self.canvas.draw()

    # --- Lógica dos Exemplos ---

    def exemplo_oscilador_geral(self):
        # Lógica SymPy
        x = sp.symbols('x')
        y = sp.Function('y')
        eq = sp.Eq(y(x).diff(x, 2) + 9*y(x), 0)
        sol = sp.dsolve(eq, y(x))
        
        # Preparar Textos
        codigo = """x = symbols('x')
y = Function('y')
# y'' + 9y = 0
eq = Eq(y(x).diff(x, 2) + 9*y(x), 0)
sol = dsolve(eq, y(x))"""
        
        # Converter solução para LaTeX
        resultado_latex = sp.latex(sol)
        self.mostrar_resultado(codigo, resultado_latex)

    def exemplo_oscilador_pvi(self):
        x = sp.symbols('x')
        y = sp.Function('y')
        eq = sp.Eq(y(x).diff(x, 2) + y(x), 0)
        
        # Condições: y(0)=1, y'(0)=0
        ics = {y(0): 1, y(x).diff(x).subs(x, 0): 0}
        sol = sp.dsolve(eq, y(x), ics=ics)
        
        codigo = """# y'' + y = 0
# y(0)=1, y'(0)=0
eq = Eq(y(x).diff(x, 2) + y(x), 0)
ics = {y(0): 1, y(x).diff(x).subs(x, 0): 0}
sol = dsolve(eq, y(x), ics=ics)"""
        
        resultado_latex = sp.latex(sol)
        self.mostrar_resultado(codigo, resultado_latex)

    def exemplo_capa_livro(self):
        # A equação da capa: d4y/dx4 + 2d2y/dx2 + y = 8sin(x) - 16cos(x)
        x = sp.symbols('x')
        y = sp.Function('y')
        
        lhs = y(x).diff(x, 4) + 2*y(x).diff(x, 2) + y(x)
        rhs = 8*sp.sin(x) - 16*sp.cos(x)
        
        eq = sp.Eq(lhs, rhs)
        sol = sp.dsolve(eq, y(x))
        
        codigo = """# Equação da Capa do Livro
# y'''' + 2y'' + y = 8sin(x) - 16cos(x)
lhs = y(x).diff(x, 4) + 2*y(x).diff(x, 2) + y(x)
rhs = 8*sin(x) - 16*cos(x)
eq = Eq(lhs, rhs)
sol = dsolve(eq, y(x))"""
        
        # A solução dessa é grande, vamos quebrar linha no LaTeX se precisar
        resultado_latex = sp.latex(sol)
        
        # Pequeno ajuste para caber na tela se for muito longa
        if len(resultado_latex) > 80:
            resultado_latex = resultado_latex.replace("C_{1}", "\\n C_{1}")
            
        self.mostrar_resultado(codigo, resultado_latex)

if __name__ == "__main__":
    root = tk.Tk()
    # Tenta configurar ícone se existir, senão ignora
    # root.iconbitmap('icone.ico') 
    app = EDOStudyApp(root)
    root.mainloop()