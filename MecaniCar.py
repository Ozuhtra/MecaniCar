import tkinter as tk    # Bibliotecas
from tkinter import messagebox, simpledialog, PhotoImage
import webbrowser

def fechar_janela():    # Confirma sair do app
    if messagebox.askyesno("Confirmação", "Deseja mesmo sair do MecaniCar?"):
        janela.destroy()

def resistencia_cabo(): # Calcula a resistividade do cabo
    janela_opcoes = tk.Toplevel(janela)
    janela_opcoes.title("Calculadora de Resistência do Cabo")
    janela_opcoes.geometry("400x300") # Aumentei um pouco para caber os botões
    janela_opcoes.configure(bg="#2c3e50")
    janela_opcoes.transient(janela)

    tk.Label(janela_opcoes, text="Selecione o material do condutor:", 
             fg="white", bg="#2c3e50", font=("Arial", 10, "bold")).pack(pady=15)

    def executar_calculo(material, rho):
        try:
            comprimento = simpledialog.askfloat("MecaniCar", f"Comprimento do cabo de {material} (em metros):", minvalue=0.01)
            if comprimento is None: return

            bitola = simpledialog.askfloat("MecaniCar", "Bitola/Área do fio (em mm²):", minvalue=0.1)
            if bitola is None: return

            resistencia = rho * (comprimento / bitola)

            mensagem_cabo = f"""
            Relatório Mecanicar
            ---------------------------------------------------
            Material: {material}
            Comprimento: {comprimento:.2f} m
            Tamanho da bitola: {bitola:.2f} mm²
            Resistência: {resistencia:.6f} Ω
            Nota: Valores acima de 0.1 Ω em cabos de 
            potência podem indicar queda de tensão crítica."""
            
            messagebox.showinfo("Diagnóstico", mensagem_cabo)
            janela_opcoes.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Problema no cálculo: {e}")

    def bitola_ajuda():
        texto_ajuda = f"""Guia de Bitolas Comuns:
    --------------------------
    Bateria/Partida: 25mm² a 50mm²
    Faróis/Grandes Cargas: 2.5mm² a 4.0mm²
    Sensores/Sinais: 0.5mm² a 1.0mm²
        
    Dica: A bitola costuma estar escrita 
    no isolamento do cabo!"""
        
        messagebox.showinfo("Ajuda com tamanho da bitola", texto_ajuda)

    tk.Button(janela_opcoes, text="COBRE (rho=0.0172)", width=25, bg="#b87333", fg="white",
              command=lambda: executar_calculo("Cobre", 0.0172)).pack(pady=5)
    
    tk.Button(janela_opcoes, text="ALUMÍNIO (rho=0.0282)", width=25, bg="#a5a9b4", fg="black",
              command=lambda: executar_calculo("Alumínio", 0.0282)).pack(pady=5)
    
    tk.Button(janela_opcoes, text="PRATA (rho=0.0159)", width=25, bg="#e5e4e2", fg="black",
              command=lambda: executar_calculo("Prata", 0.0159)).pack(pady=5)
    
    tk.Button(janela_opcoes, text="Guia de tamanho de bitolas", width=40, bg="#00c421", fg="black",
              command=bitola_ajuda).pack(pady=15)

def conversor_temperatura():    # Conversor °C para °F
    janela_opcoes = tk.Toplevel(janela)
    janela_opcoes.title("Conversor de Força")
    janela_opcoes.geometry("300x200")
    janela_opcoes.configure(bg="#2c3e50")

    janela_opcoes.transient(janela)

    tk.Label(janela_opcoes, text="Selecione a conversão:",
             fg="white", bg="#2c3e50", font=("Arial", 10, "bold")).pack(pady=15)

    def executar_calculo(modo):
        if modo == "C_F":
            valor = simpledialog.askfloat("MecaniCar", "Digite o valor em °C", minvalue=0.1)
            if valor is not None:
                resultado = (valor * 1.8) + 32
                mensagem_c = f"""
                Relatório MecaniCar
                ---------------------------------------------------
                Resultado: {valor:.2f} °C = {resultado:.2f} °F"""

                messagebox.showinfo("Diagnóstico", mensagem_c)
        else:
            valor = simpledialog.askfloat("MecaniCar", "Digite o valor em °F", minvalue=0.1)
            if valor is not None:
                resultado = (valor - 32) * 5/9
                mensagem_f = f"""
                Relatório MecaniCar
                ---------------------------------------------------
                Resultado: {valor} °F = {resultado} °C"""
                
                messagebox.showinfo("Diagnóstico", mensagem_f)

    tk.Button(janela_opcoes, text="°C -> °F", width=20, bg="#061824", fg="white",
              command=lambda: executar_calculo("C_F")).pack(pady=5)
    tk.Button(janela_opcoes, text="°F -> °C", width=20, bg="#061824", fg="white",
              command=lambda: executar_calculo("F_C")).pack(pady=5)
 
def conversor_forca():  # Conversor NM para KGFM
    janela_opcoes = tk.Toplevel(janela)
    janela_opcoes.title("Conversor de Força")
    janela_opcoes.geometry("300x200")
    janela_opcoes.configure(bg="#2c3e50")

    janela_opcoes.transient(janela)

    tk.Label(janela_opcoes, text="Selecione a conversão:",
             fg="white", bg="#2c3e50", font=("Arial", 10, "bold")).pack(pady=15)
    
    def executar_calculo(modo):
        if modo == "NM_KGFM":
            valor = simpledialog.askfloat("MecaniCar", "Digite o valor em NM", minvalue=0.1)
            if valor is not None:
                resultado = valor * 0.101972
                mensagem_nm = f"""
                Relatório MecaniCar
                ---------------------------------------------------
                Resultado: {valor:.2f} NM = {resultado:.2f} KGFM"""

                messagebox.showinfo("Diagnóstico", mensagem_nm)
                janela_opcoes.destroy()
        else:
                valor = simpledialog.askfloat("MecaniCar", "Digite o valor em KGFM", minvalue=0.1)
                if valor is not None:
                    resultado = valor * 9.8067
                    mensagem_kgfm = f"""
                Relatório MecaniCar
                ---------------------------------------------------
                Resultado: {valor:.2f} KGFM = {resultado:.2f} NM"""
                    
                messagebox.showinfo("Diagnóstico", mensagem_kgfm)
        
    tk.Button(janela_opcoes, text="NM -> KGFM", width=20, bg="#061824", fg="white",
              command=lambda: executar_calculo("NM_KGFM")).pack(pady=5)
    
    tk.Button(janela_opcoes, text="KGFM -> NM", width=20, bg="#061824", fg="white",
              command=lambda: executar_calculo("KGFM_NM")).pack(pady=5)

def conversor_potencia():   # Conversor CV para HP
    janela_opcoes = tk.Toplevel(janela)
    janela_opcoes.title("Conversor de Potência")
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
                mensagem_hp = f"""
                Relatório MecaniCar
                ---------------------------------------------------
                Resultado: {valor:.2f} HP = {resultado:.2f} CV"""
                
                messagebox.showinfo("Diagnóstico", mensagem_hp)

                janela_opcoes.destroy()
        else:
            valor = simpledialog.askfloat("MecaniCar", "Digite o valor em CV:", minvalue=0.0)
            if valor is not None:
                resultado = valor * 0.98632
                mensagem_cv = f"""
                Relatório MecaniCar
                ---------------------------------------------------
                Resultado: {valor:.2f} CV = {resultado:.2f} HP"""
                
                messagebox.showinfo("Diagnóstico", mensagem_cv)

    tk.Button(janela_opcoes, text="HP -> CV", width=20, bg="#061824", fg="white",
              command=lambda: executar_calculo("HP_CV")).pack(pady=5)
    
    tk.Button(janela_opcoes, text="CV -> HP", width=20, bg="#061824", fg="white",
              command=lambda: executar_calculo("CV_HP")).pack(pady=5)

def conversor_pressao():    # Conversor BAR para PSI
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
                mensagem_bar = f"""
                Relatório MecaniCar
                ---------------------------------------------------
                Resultado: {valor:.2f} BAR = {resultado:.2f} PSI
                O valor padrão para pneus de carro é entre 30 a 35 PSI"""
                
                messagebox.showinfo("Diagnóstico", mensagem_bar)
                janela_opcoes.destroy()
        else:
            valor = simpledialog.askfloat("MecaniCar", "Digite o valor em PSI:", minvalue=0.0)
            if valor is not None:
                resultado = valor * 0.0689476
                mensagem_psi = f"""
            Relatório Mecanicar
            ---------------------------------------------------
            Resultado: {valor:.2f} PSI = {resultado:.2f} BAR
            O valor padrão para pneus de carro é entre 2 e 2,4 BAR"""
                
                messagebox.showinfo("Diagnóstico", mensagem_psi)
                janela_opcoes.destroy()
    
    tk.Button(janela_opcoes, text="BAR -> PSI", width=20, bg="#061824", fg="white",

              command=lambda: executar_calculo("BAR_PSI")).pack(pady=5)

    tk.Button(janela_opcoes, text="PSI -> BAR", width=20, bg="#061824", fg="white",

              command=lambda: executar_calculo("PSI_BAR")).pack(pady=5)

def calcular_dinamico(entradas, janela_calculo, tensao):    # Calcula circuito série
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
            f"Potência Total: {potencia:.2f} W\n"
            f"Tensão do circuito: {tensao} V"
        )
        messagebox.showinfo("Diagnóstico", resultado)
        janela_calculo.destroy() 
    except ValueError:
        messagebox.showerror("Erro", "Preencha os campos com números válidos.")

def calcular_paralelo_logica(entradas, janela_calculo, tensao): # Calcula circuito paralelo
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
            f"Potência Total: {potencia:.2f} W\n"
            f"Tensão do circuito: {tensao} V"
        )
        messagebox.showinfo("Diagnóstico", resultado)
        janela_calculo.destroy() 
    except ZeroDivisionError:
        messagebox.showerror("Erro", "Resistência não pode ser zero!")
    except ValueError:
        messagebox.showerror("Erro", "Preencha os campos com números válidos.")

def abrir_github(): # Abre o Github através do botão
    webbrowser.open("https://github.com/Ozuhtra/MecaniCar")

def abrir_janela_serie():   # Abre a janela p/ calcular o paralelo
    configurar_janela(calcular_dinamico, "Série")

def abrir_janela_paralelo():    # Abre a janela p/ calcular o série
    configurar_janela(calcular_paralelo_logica, "Paralelo")

def configurar_janela(funcao_calculo, tipo):    # Configurações da janela
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

janela = tk.Tk()    # Configurações janela principal
janela.title("MecaniCar")
janela.geometry("1200x800")
janela.protocol("WM_DELETE_WINDOW", fechar_janela)

try:    # Plano de fundo
    img_fundo = PhotoImage(file="mecanicar.png") 
    lbl_fundo = tk.Label(janela, image=img_fundo)
    lbl_fundo.place(x=0, y=0, relwidth=1, relheight=1)
except:
    janela.config(bg="#2c3e50")

lbl_titulo = tk.Label(janela, text="MECANICAR - A SUA SOLUÇÃO AUTOMOTIVA",  # Textos da página principal
                      font=("Helvetica", 16, "bold"), fg="white", bg="#2c3e50")
lbl_titulo.place(x=680, y=50, anchor="center")

lbl_leg_conv = tk.Label(janela, text="Conversores de unidades de medida",
                        font=("Helvetica", 14, "bold"), fg="white", bg="#004ab9")
lbl_leg_conv.place(x=1000, y=150)

lbl_leg_elet = tk.Label(janela, text="Calculadora eletroeletrônica",
                        font=("Helvetica", 14, "bold"), fg="white", bg="#004ab9")
lbl_leg_elet.place(x=20, y=150)

# ----- BOTÕES -----
btn_iniciar_serie = tk.Button(janela, text="Calcular circuito em série", 
                        command=abrir_janela_serie, 
                        width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"))
btn_iniciar_serie.place(x=120, y=420, anchor="center")

btn_iniciar_paralelo = tk.Button(janela, text="Calcular circuito em paralelo", 
                        command=abrir_janela_paralelo, 
                        width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"))
btn_iniciar_paralelo.place(x=120, y=470, anchor="center")

btn_calcular_pressao = tk.Button(janela, text="Calcular pressão", 
                                 command=conversor_pressao,
                                 width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"))
btn_calcular_pressao.place(x=1110, y=440)

btn_calcular_potencia = tk.Button(janela, text="Calcular potência",
                               command=conversor_potencia,
                               width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"))
btn_calcular_potencia.place(x=1110, y=388.5)

btn_calcular_forca = tk.Button(janela, text="Calcular força",
                               command=conversor_forca,
                               width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"))
btn_calcular_forca.place(x=1110, y=340)

btn_calcular_temperatura = tk.Button(janela, text="Calcular temperatura",
                                     command=conversor_temperatura,
                                     width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"))
btn_calcular_temperatura.place(x=1110, y=290)

btn_calcular_cabo = tk.Button(janela, text="Calcular resistividade do cabo", 
                              command=resistencia_cabo,
                              width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"))
btn_calcular_cabo.place(x=-10, y=345)

btn_versao_app = tk.Button(janela, text="v.0.0.3a",
                           command=abrir_github,
                           fg="red", font=("Arial", 12, "bold"))
btn_versao_app.place(x=1290, y=680)

btn_sair = tk.Button(janela, text="Fechar", command=fechar_janela, fg="red")
btn_sair.place(x=680, y=650, anchor="center")

def sobre_eu():
    messagebox.showinfo("Pedro Michelin", "Sou o Pedro, amante de carros, eletroeletrônica, programação e futuro Engenheiro Elétrico!.")

def sobre_olavo():
    messagebox.showinfo("Pedro Henrique", "Coloque seu texto aqui!!")

btn_sobre_eu = tk.Button(janela, text="Sobre o Pedro Michelin", command=sobre_eu, fg="blue")
btn_sobre_eu.place(x=520, y=670)

btn_sobre_olavo = tk.Button(janela, text="Sobre o Pedro Henrique", command=sobre_olavo, fg="pink")
btn_sobre_olavo.place(x=705, y=670)

janela.mainloop()