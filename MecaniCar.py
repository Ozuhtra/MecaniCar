import tkinter as tk
from tkinter import messagebox, simpledialog, PhotoImage

# --- FUNÇÕES DE LÓGICA E CÁLCULO ---

def fechar_janela():
    if messagebox.askyesno("Confirmação", "Deseja mesmo sair do MecaniCar?"):
        janela.destroy()

def conversor_forca():
    janela_opcoes = tk.Toplevel(janela)
    janela_opcoes.title("Conversor de Força")
    janela_opcoes.geometry("300x200")
    janela_opcoes.configure(bg="#2c3e50")

    janela_opcoes.transient(janela)

    tk.Label(janela_opcoes, text="Selecione a conversão:", 
             fg="white", bg="#2c3e50", font=("Arial", 10, "bold")).pack(pady=15)
    
    def executar_calculo(modo):
        if modo == "HP_CV":
            valor = simpledialog.askfloat("MecaniCar", "Digite o valor em HP:", minvalue=0.0)
            if valor is not None:
                resultado = valor * 1.01387
                messagebox.showinfo("Relatório MecaniCar \n"
                                    "--------------------------\n"
                                    "Resultado", f"{valor:.2f} HP = {resultado:.2f} CV")
                janela_opcoes.destroy()
        else:
            valor = simpledialog.askfloat("MecaniCar", "Digite o valor em CV:", minvalue=0.0)
            if valor is not None:
                resultado = valor * 0.98632
                messagebox.showinfo("Relatório MecaniCar \n"
                                    "--------------------------\n"
                                    "Resultado", f"{valor:.2f} CV = {resultado:.2f} HP")

    tk.Button(janela_opcoes, text="HP -> CV", width=20, bg="#061824", fg="white",
              command=lambda: executar_calculo("HP_CV")).pack(pady=5)
    
    tk.Button(janela_opcoes, text="CV -> HP", width=20, bg="#061824", fg="white",
              command=lambda: executar_calculo("CV_HP")).pack(pady=5)

def conversor_pressao():
    """Cria uma janelinha de escolha para o mecânico"""
    janela_opcoes = tk.Toplevel(janela)
    janela_opcoes.title("Conversão de Pressão")
    janela_opcoes.geometry("300x200")
    janela_opcoes.configure(bg="#2c3e50")
    
    # Deixa a janela centralizada em relação à principal
    janela_opcoes.transient(janela)

    tk.Label(janela_opcoes, text="Selecione a conversão:", 
             fg="white", bg="#2c3e50", font=("Arial", 10, "bold")).pack(pady=15)

    def executar_calculo(modo):
        if modo == "BAR_PSI":
            valor = simpledialog.askfloat("MecaniCar", "Digite o valor em BAR:", minvalue=0.0)
            if valor is not None:
                resultado = valor * 14.5038
                messagebox.showinfo("Relatório MecaniCar \n"
                                    "--------------------------\n"
                                    "Resultado", f"{valor:.2f} BAR = {resultado:.2f} PSI"
                                    "O valor padrão para pneus de carro é entre 30 a 35 PSI")
                janela_opcoes.destroy()
        else:
            valor = simpledialog.askfloat("MecaniCar", "Digite o valor em PSI:", minvalue=0.0)
            if valor is not None:
                resultado = valor * 0.0689476
                messagebox.showinfo("Relatório Mecanicar \n"
                                    "--------------------------\n"
                                    "Resultado", f"{valor:.2f} PSI = {resultado:.2f} BAR"
                                    "O valor padrão para pneus de carro é entre 2 e 2,4 BAR")
                janela_opcoes.destroy()

    # Botões de opção
    tk.Button(janela_opcoes, text="BAR -> PSI", width=20, bg="#061824", fg="white",
              command=lambda: executar_calculo("BAR_PSI")).pack(pady=5)
    
    tk.Button(janela_opcoes, text="PSI -> BAR", width=20, bg="#061824", fg="white",
              command=lambda: executar_calculo("PSI_BAR")).pack(pady=5)

def calcular_dinamico(entradas, janela_calculo, tensao):
    try:
        valores = [float(en.get().replace(',', '.')) for en in entradas if en.get()]
        if not valores: return
        
        req = sum(valores)
        corrente = tensao / req
        fusivel1, fusivel2 = corrente * 1.20, corrente * 1.50
        potencia = (tensao ** 2) / req

        resultado = (
            f"Relatório MecaniCar:\n"
            f"--------------------------\n"
            f"Resistência Total: {req:.2f} Ω\n"
            f"Corrente: {corrente:.2f} A\n"
            f"Fusível Sugerido: {fusivel1:.2f} a {fusivel2:.2f} A\n"
            f"Potência Total: {potencia:.2f} W"
        )
        messagebox.showinfo("Diagnóstico", resultado)
        janela_calculo.destroy() 
    except ValueError:
        messagebox.showerror("Erro", "Preencha os campos com números válidos.")

def calcular_paralelo_logica(entradas, janela_calculo, tensao):
    try:
        valores = [float(en.get().replace(',', '.')) for en in entradas if en.get()]
        if not valores: return
        
        soma_inversos = sum(1/r for r in valores if r > 0)
        req_paralelo = 1 / soma_inversos
        
        corrente = tensao / req_paralelo
        fusivel1, fusivel2 = corrente * 1.20, corrente * 1.50
        potencia = (tensao ** 2) / req_paralelo

        resultado = (
            f"Relatório MecaniCar:\n"
            f"--------------------------\n"
            f"Resistência Total: {req_paralelo:.2f} Ω\n"
            f"Corrente: {corrente:.2f} A\n"
            f"Fusível Sugerido: {fusivel1:.2f} a {fusivel2:.2f} A\n"
            f"Potência Total: {potencia:.2f} W"
        )
        messagebox.showinfo("Diagnóstico", resultado)
        janela_calculo.destroy() 
    except ZeroDivisionError:
        messagebox.showerror("Erro", "Resistência não pode ser zero!")
    except ValueError:
        messagebox.showerror("Erro", "Preencha os campos com números válidos.")

# --- FUNÇÕES PARA ABRIR JANELAS DE CIRCUITOS ---

def abrir_janela_serie():
    configurar_janela(calcular_dinamico, "Série")

def abrir_janela_paralelo():
    configurar_janela(calcular_paralelo_logica, "Paralelo")

def configurar_janela(funcao_calculo, tipo):
    try:
        tensao = simpledialog.askfloat("MecaniCar", "Tensão do sistema (V):", minvalue=0.1)
        if tensao is None: return
        num_res = simpledialog.askinteger("MecaniCar", "Quantos resistores tem na associação?", minvalue=1)
        if num_res is None: return

        nova_janela = tk.Toplevel(janela)
        nova_janela.title(f"Entrada {tipo}")
                
        entradas = []
        for i in range(num_res):
            tk.Label(nova_janela, text=f"Resistor {i+1} (Ω):").pack(pady=2)
            en = tk.Entry(nova_janela)
            en.pack(pady=2)
            entradas.append(en)

        tk.Button(nova_janela, text="CALCULAR", bg="blue", fg="white", font=("Arial", 15, "bold"),
                  command=lambda: funcao_calculo(entradas, nova_janela, tensao)).pack(pady=10)
    except Exception as e:
        messagebox.showerror("Erro", f"Problema: {e}")

# --- CONFIGURAÇÃO DA JANELA PRINCIPAL ---

janela = tk.Tk()
janela.title("MecaniCar")
janela.geometry("1200x800")
janela.protocol("WM_DELETE_WINDOW", fechar_janela)

try:
    img_fundo = PhotoImage(file="mecanicar.png") 
    lbl_fundo = tk.Label(janela, image=img_fundo)
    lbl_fundo.place(x=0, y=0, relwidth=1, relheight=1)
except:
    janela.config(bg="#2c3e50")

# Título
lbl_titulo = tk.Label(janela, text="MECANICAR - A SUA SOLUÇÃO AUTOMOTIVA", 
                      font=("Helvetica", 16, "bold"), fg="white", bg="#2c3e50")
lbl_titulo.place(x=680, y=50, anchor="center")

# Botões Lado Esquerdo (Circuitos)
btn_iniciar_serie = tk.Button(janela, text="Calcular circuito em série", 
                        command=abrir_janela_serie, 
                        width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"))
btn_iniciar_serie.place(x=120, y=420, anchor="center")

btn_iniciar_paralelo = tk.Button(janela, text="Calcular circuito em paralelo", 
                        command=abrir_janela_paralelo, 
                        width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"))
btn_iniciar_paralelo.place(x=120, y=470, anchor="center")

# Botão Lado Direito (Pressão)
btn_calcular_pressao = tk.Button(janela, text="Calcular pressão", 
                                 command=conversor_pressao,
                                 width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"))
btn_calcular_pressao.place(x=950, y=440) # Ajustei levemente o X para caber na tela padrão

btn_calcular_forca = tk.Button(janela, text="Calcular força",
                               command=conversor_forca,
                               width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"))
btn_calcular_forca.place(x=950, y=388.5)
# Botão Sair
btn_sair = tk.Button(janela, text="Fechar", command=fechar_janela, fg="red")
btn_sair.place(x=680, y=650, anchor="center")

# Botões de Créditos
def sobre_eu():
    messagebox.showinfo("Pedro Michelin", "Sou o Pedro, amante de carros, eletroeletrônica, programação e futuro Engenheiro Elétrico!.")

def sobre_olavo():
    messagebox.showinfo("Pedro Henrique", "Coloque seu texto aqui!!")

btn_sobre_eu = tk.Button(janela, text="Sobre o Pedro Michelin", command=sobre_eu, fg="blue")
btn_sobre_eu.place(x=520, y=670)

btn_sobre_olavo = tk.Button(janela, text="Sobre o Pedro Henrique", command=sobre_olavo, fg="pink")
btn_sobre_olavo.place(x=705, y=670)

janela.mainloop()