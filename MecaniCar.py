import tkinter as tk    # Bibliotecas
from tkinter import messagebox, simpledialog, PhotoImage
import webbrowser
import pygame
from datetime import datetime
from fpdf import FPDF
import os

class SimuladorParalelo:    # Faz a animação do circuito paralelo
    def __init__(self, dados):
        self.dados = dados
        self.C_FUNDO = (10, 15, 25)
        self.C_FIO = (160, 160, 160)
        self.C_ELETRON = (0, 255, 255)
        self.C_VALOR = (0, 255, 180)
        self.C_TEXTO = (220, 220, 220)
        self.C_TOOLTIP = (30, 35, 50) # Cor do balão de info
        self.ligado = False

    def desenhar_tooltip(self, tela, fonte, pos, titulo, linhas):
        x, y = pos[0] + 15, pos[1] + 15
        largura, altura = 220, 30 + (len(linhas) * 20)
        # Desenha fundo do balão
        pygame.draw.rect(tela, self.C_TOOLTIP, (x, y, largura, altura), 0, 8)
        pygame.draw.rect(tela, self.C_FIO, (x, y, largura, altura), 1, 8)
        # Texto dentro do balão
        tela.blit(fonte.render(titulo, True, self.C_VALOR), (x + 10, y + 5))
        for i, linha in enumerate(linhas):
            tela.blit(fonte.render(linha, True, self.C_TEXTO), (x + 10, y + 28 + (i * 18)))

    def iniciar(self):
        pygame.init()
        tela = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("MecaniCar - Simulação Paralela")
        relogio = pygame.time.Clock()
        
        fonte_info = pygame.font.SysFont("Arial", 20, bold=True)
        fonte_res = pygame.font.SysFont("Arial(bold)", 22)
        fonte_bateria = pygame.font.SysFont("Arial", 16, bold=True)
        fonte_sinal = pygame.font.SysFont("Arial", 22, bold=True)

        # 15 elétrons distribuídos pelos ramos
        num_r = len(self.dados['resistores'])
        eletrons = []
        for i in range(15):
            eletrons.append({
                'ramo': i % num_r, # Distribui entre os caminhos disponíveis
                'pos_path': i * (1.0 / 15)
            })

        rodando = True
        while rodando:
            m_pos = pygame.mouse.get_pos() # Posição do mouse
            tela.fill(self.C_FUNDO)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: rodando = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.ligado = not self.ligado

            pygame.draw.rect(tela, self.C_FIO, (320, 150, 600, 300), 4)
            
            if self.ligado:
                x_seta = 450 
                y_seta = 165 # Altura do fio de cima
                
                txt_seta_simples = fonte_sinal.render("---->", True, (255, 255, 0)) # Amarelo
                texto_formatado = f"{float(self.dados['corrente']):.2f}A"
                txt_v_seta = fonte_res.render(texto_formatado, True, (255, 255, 0))

                tela.blit(txt_seta_simples, (x_seta, y_seta - 12)) 
                tela.blit(txt_v_seta, (x_seta, y_seta + 10))

            # Símbolo da Bateria (Igual ao Série)
            pygame.draw.line(tela, self.C_VALOR, (320 - 20, 290), (320 + 20, 290), 3)
            pygame.draw.line(tela, self.C_VALOR, (320 - 10, 310), (320 + 10, 310), 6)

            txt_tensao = fonte_bateria.render(f"{self.dados['tensao']}V", True, self.C_VALOR)
            tela.blit(txt_tensao, (185, 290))

            # Polo Positivo (+) e Negativo (-)
            txt_mais = fonte_sinal.render("+", True, (255, 50, 50))
            tela.blit(txt_mais, (275, 275)) 

            txt_menos = fonte_sinal.render("-", True, (100, 100, 255))
            tela.blit(txt_menos, (275, 305)) # Próximo ao polo inferior

            pygame.draw.rect(tela, (20, 30, 50), (20, 20, 260, 150), 0, 10)
            pygame.draw.rect(tela, self.C_VALOR, (20, 20, 260, 150), 2, 10)

            # Resultados dentro da borda verde
            potencia_total = self.dados['tensao'] * self.dados['corrente']
            tela.blit(fonte_info.render("Resultados:", True, self.C_VALOR), (40, 35))
            tela.blit(fonte_res.render(f"Tensão: {self.dados['tensao']} V", True, self.C_TEXTO), (40, 65))
            tela.blit(fonte_res.render(f"Corrente Total: {self.dados['corrente']:.2f} A", True, self.C_TEXTO), (40, 85))
            tela.blit(fonte_res.render(f"Resistência Total: {self.dados['req']:.2f} Ω", True, self.C_TEXTO), (40, 105))
            tela.blit(fonte_res.render(f"Potência Total: {potencia_total:.2f} W", True, self.C_VALOR), (40, 130))
            tela.blit(fonte_res.render("Aperte 'espaço' para iniciar", True, self.C_TEXTO), (380, 80))
            # Colisão do mouse
            resistor_hover = None
            espacamento = 600 / (num_r + 1)
            
            for i, r in enumerate(self.dados['resistores']):
                px = 320 + espacamento * (i + 1)
                py = 285 # Centralizado na altura do circuito
                
                # Fio vertical do ramo
                pygame.draw.line(tela, self.C_FIO, (px, 150), (px, 450), 2)
                
                # Retângulo do Resistor (Retângulo de colisão igual ao série)
                r_rect = pygame.Rect(px - 25, py, 50, 30)
                
                cor_borda = (255, 255, 255) if r_rect.collidepoint(m_pos) else self.C_FIO
                pygame.draw.rect(tela, (40, 45, 60), r_rect)
                pygame.draw.rect(tela, cor_borda, r_rect, 2)
                
                # Lógica de Hover (Tooltip)
                if r_rect.collidepoint(m_pos):
                    corrente_r = self.dados['tensao'] / r
                    pot_r = self.dados['tensao'] * corrente_r
                    resistor_hover = (f"RESISTOR R{i+1}", [
                        f"Corrente: {corrente_r:.2f} A", 
                        f"Potência: {pot_r:.2f} W", 
                        f"Valor: {r} Ω"
                    ])
                # Texto R1, R2, etc. (Usando fonte_res e alinhamento do Série)
                tela.blit(fonte_res.render(f"R{i+1}", True, self.C_TEXTO), (px - 10, py + 35))

            # 4. Elétrons (Velocidade constante e tamanho do Série)
            if self.ligado:
                vel = 0.005 # Velocidade fixa e suave, conforme padrão visual
                for e in eletrons:
                    e['pos_path'] = (e['pos_path'] + vel) % 1.0
                    p = e['pos_path']
                    x_r = 320 + espacamento * (e['ramo'] + 1)
                    
                    if p < 0.25: # Superior
                        x, y = 320 + (x_r - 320) * (p/0.25), 150
                    elif p < 0.50: # Descendo Ramo
                        x, y = x_r, 150 + (300 * ((p-0.25)/0.25))
                    elif p < 0.75: # Inferior
                        x, y = x_r - (x_r - 320) * ((p-0.50)/0.25), 450
                    else: # Subindo Bateria
                        x, y = 320, 450 - (300 * ((p-0.75)/0.25))
                    
                    # Desenha elétron (Raio 4, igual ao série)
                    pygame.draw.circle(tela, self.C_ELETRON, (int(x), int(y)), 4)

            # 5. Desenha o balão de Hover por último (para ficar na frente de tudo)
            if resistor_hover:
                self.desenhar_tooltip(tela, fonte_res, m_pos, resistor_hover[0], resistor_hover[1])

            pygame.display.flip()
            relogio.tick(60)
        pygame.display.quit()

class SimuladorGrafico: # Faz a animação do circuito série
    def __init__(self, dados):
        self.dados = dados
        self.C_FUNDO = (10, 15, 25)
        self.C_FIO = (160, 160, 160)
        self.C_ELETRON = (0, 255, 255)
        self.C_VALOR = (0, 255, 180)
        self.C_TEXTO = (220, 220, 220)
        self.C_TOOLTIP = (30, 35, 50) # Cor do balão de info
        self.ligado = False

    def desenhar_tooltip(self, tela, fonte, pos, titulo, linhas):
        """ Desenha o balão de informações (Hover) """
        x, y = pos[0] + 15, pos[1] + 15
        largura, altura = 220, 30 + (len(linhas) * 20)
        # Desenha fundo do balão
        pygame.draw.rect(tela, self.C_TOOLTIP, (x, y, largura, altura), 0, 8)
        pygame.draw.rect(tela, self.C_FIO, (x, y, largura, altura), 1, 8)
        # Texto dentro do balão
        tela.blit(fonte.render(titulo, True, self.C_VALOR), (x + 10, y + 5))
        for i, linha in enumerate(linhas):
            tela.blit(fonte.render(linha, True, self.C_TEXTO), (x + 10, y + 28 + (i * 18)))

    def iniciar(self):
        pygame.init()
        tela = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("MecaniCar")
        relogio = pygame.time.Clock()
        fonte_info = pygame.font.SysFont("Arial", 20, bold=True)
        fonte_res = pygame.font.SysFont("Arial(bold)", 22)
        
        eletrons = [{'pos_path': i * (1.0 / 15)} for i in range(15)]
        rodando = True
        
        while rodando:
            m_pos = pygame.mouse.get_pos() # Posição do mouse
            tela.fill(self.C_FUNDO)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: rodando = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.ligado = not self.ligado

            # 1. Circuito e Bateria
            pygame.draw.rect(tela, self.C_FIO, (320, 150, 600, 300), 4)
            # --- INDICAÇÃO DE FLUXO (SETA SIMPLES) ---
            if self.ligado:
                # Definimos a posição no fio superior
                x_seta = 450 
                y_seta = 165 # Altura do fio de cima

                # 1. Renderiza a seta -->
                # Usei a fonte_sinal para a seta ficar maior e visível
                txt_seta_simples = fonte_sinal.render("---->", True, (255, 255, 0)) # Amarelo
                
                # 2. Renderiza a tensão (ex: 12V)
                txt_v_seta = fonte_res.render(f"{float(self.dados['corrente']):.2f}A", True, (255, 255, 0))

                # 3. 'Cola' na tela (Blit)
                # Centraliza a seta no fio (ajuste o -5 ou -10 se precisar subir/descer a seta)
                tela.blit(txt_seta_simples, (x_seta, y_seta - 12)) 
                
                # Coloca a tensão logo abaixo da seta
                tela.blit(txt_v_seta, (x_seta, y_seta + 10))
            # Símbolo da Bateria
            pygame.draw.line(tela, self.C_VALOR, (320 - 20, 290), (320 + 20, 290), 3)
            pygame.draw.line(tela, self.C_VALOR, (320 - 10, 310), (320 + 10, 310), 6)

            fonte_bateria = pygame.font.SysFont("Arial", 16, bold=True)
            fonte_sinal = pygame.font.SysFont("Arial", 22, bold=True)

            txt_tensao = fonte_bateria.render(f"{self.dados['tensao']}V", True, self.C_VALOR)
            # Coloca o texto um pouco à esquerda (x=180) e centralizado na altura da bateria (y=290)
            tela.blit(txt_tensao, (185, 290))
            # 2. Painel Principal (Com Potência Total)
            pygame.draw.rect(tela, (20, 30, 50), (20, 20, 260, 150), 0, 10)
            pygame.draw.rect(tela, self.C_VALOR, (20, 20, 260, 150), 2, 10)

            txt_mais = fonte_sinal.render("+", True, (255, 50, 50))
            tela.blit(txt_mais, (275, 275)) 

            # 3. Sinal de Negativo (-) em Azul
            txt_menos = fonte_sinal.render("-", True, (100, 100, 255))
            tela.blit(txt_menos, (275, 305)) # Próximo ao polo inferior
            
            potencia_total = self.dados['tensao'] * self.dados['corrente']
            
            tela.blit(fonte_info.render("Resultados:", True, self.C_VALOR), (40, 35))
            tela.blit(fonte_res.render(f"Tensão: {self.dados['tensao']} V", True, self.C_TEXTO), (40, 65))
            tela.blit(fonte_res.render(f"Corrente Total: {self.dados['corrente']:.2f} A", True, self.C_TEXTO), (40, 85))
            tela.blit(fonte_res.render(f"Resistência Total: {self.dados['req']:.2f} Ω", True, self.C_TEXTO), (40, 105))
            tela.blit(fonte_res.render(f"Potência Total: {potencia_total:.2f} W", True, self.C_VALOR), (40, 130))
            tela.blit(fonte_res.render("Aperte 'espaço' para iniciar", True, self.C_TEXTO), (380, 80))

            # 3. Resistores e Lógica de Hover
            resistor_hover = None
            for i, r in enumerate(self.dados['resistores']):
                px = 320 + (600 / (len(self.dados['resistores']) + 1)) * (i + 1)
                py = 450
                r_rect = pygame.Rect(px - 25, py - 15, 50, 30)
                
                # Se o mouse estiver em cima, muda a cor da borda
                cor_borda = (255, 255, 255) if r_rect.collidepoint(m_pos) else self.C_FIO
                pygame.draw.rect(tela, (40, 45, 60), r_rect)
                pygame.draw.rect(tela, cor_borda, r_rect, 2)
                
                # Guarda qual resistor está com o mouse em cima para mostrar o balão depois
                if r_rect.collidepoint(m_pos):
                    # Cálculos para o resistor específico (Circuito Série: I é a mesma)
                    queda_v = self.dados['corrente'] * r
                    pot_r = queda_v * self.dados['corrente']
                    resistor_hover = (f"RESISTOR R{i+1}", [f"Queda: {queda_v:.2f} V", f"Potência: {pot_r:.2f} W", f"Valor: {r} Ω"])

                tela.blit(fonte_res.render(f"R{i+1}", True, self.C_TEXTO), (px - 10, py + 20))

            # 4. Elétrons (Velocidade Ajustada - Mais lenta)
            if self.ligado:
                # Diminuí o fator de multiplicação para a animação ficar suave
                vel = 0.001 + (self.dados['corrente'] * 0.0005) 
                if vel > 0.015: vel = 0.015 # Limite para não ficar rápido demais
                
                for e in eletrons:
                    e['pos_path'] = (e['pos_path'] + vel) % 1.0
                    p = e['pos_path']
                    if p < 0.33: x, y = 320 + (600 * (p/0.33)), 150
                    elif p < 0.50: x, y = 920, 150 + (300 * ((p-0.33)/0.17))
                    elif p < 0.83: x, y = 920 - (600 * ((p-0.50)/0.33)), 450
                    else: x, y = 320, 450 - (300 * ((p-0.83)/0.17))
                    pygame.draw.circle(tela, self.C_ELETRON, (int(x), int(y)), 4)

            # 5. Desenha o balão de Hover por último (para ficar na frente de tudo)
            if resistor_hover:
                self.desenhar_tooltip(tela, fonte_res, m_pos, resistor_hover[0], resistor_hover[1])

            pygame.display.flip()
            relogio.tick(60)
        pygame.display.quit()

def fechar_janela():    # Confirma sair do app
    if messagebox.askyesno("Confirmação", "Deseja mesmo sair do MecaniCar?"):
        janela.destroy()

def triangulo_formulas():   # Calcula Lei de Ohm
    janela_calc = tk.Toplevel()
    janela_calc.title("Calculadora de Lei de Ohm")
    janela_calc.geometry("550x400")
    janela_calc.configure(bg="#2c3e50")
    janela_calc.resizable(False, False)

    tk.Label(janela_calc, text="O QUE VOCÊ DESEJA CALCULAR?", font=("Arial", 14, "bold"), 
             bg="#121212", fg="#00ffb4").pack(pady=20)

    def interagir(tipo):
        try:
            if tipo == "U":
                r = simpledialog.askfloat("MecaniCar", "Informe a Resistência (Ω):")
                i = simpledialog.askfloat("MecaniCar", "Informe a Corrente (A):")
                if r is not None and i is not None:
                    messagebox.showinfo("Resultado", f"Tensão (U) = {r * i:.2f} V")
            
            elif tipo == "R":
                u = simpledialog.askfloat("MecaniCar", "Informe a Tensão (V):")
                i = simpledialog.askfloat("MecaniCar", "Informe a Corrente (A):")
                if u is not None and i is not None:
                    res = u / i if i > 0 else 0
                    messagebox.showinfo("Resultado", f"Resistência (R) = {res:.2f} Ω")

            elif tipo == "I_URI":
                u = simpledialog.askfloat("MecaniCar", "Informe a Tensão (V):")
                r = simpledialog.askfloat("MecaniCar", "Informe a Resistência (Ω):")
                if u is not None and r is not None:
                    res = u / r if r > 0 else 0
                    messagebox.showinfo("Resultado", f"Corrente (I) = {res:.2f} A")

            elif tipo == "P":
                u = simpledialog.askfloat("MecaniCar", "Informe a Tensão (V):")
                i = simpledialog.askfloat("MecaniCar", "Informe a Corrente (A):")
                if u is not None and i is not None:
                    messagebox.showinfo("Resultado", f"Potência (P) = {u * i:.2f} W")

            elif tipo == "U_PUI":
                p = simpledialog.askfloat("MecaniCar", "Informe a Potência (W):")
                i = simpledialog.askfloat("MecaniCar", "Informe a Corrente (A):")
                if p is not None and i is not None:
                    res = p / i if i > 0 else 0
                    messagebox.showinfo("Resultado", f"Tensão (U) = {res:.2f} V")

            elif tipo == "I_PUI":
                p = simpledialog.askfloat("MecaniCar", "Informe a Potência (W):")
                u = simpledialog.askfloat("MecaniCar", "Informe a Tensão (V):")
                if p is not None and u is not None:
                    res = p / u if u > 0 else 0
                    messagebox.showinfo("Resultado", f"Corrente (I) = {res:.2f} A")

        except Exception as e:
            messagebox.showerror("Erro", "Ocorreu um erro no cálculo.")

    estilo_topo = {"font": ("Arial", 16, "bold"), "width": 6, "height": 2, "bd": 0, "cursor": "hand2"}
    estilo_base = {"font": ("Arial", 16, "bold"), "width": 5, "height": 2, "bd": 0, "cursor": "hand2"}

    tk.Button(janela_calc, text="U", bg="#FFD700", fg="black", **estilo_topo, command=lambda: interagir("U")).place(x=100, y=130)
    tk.Button(janela_calc, text="R", bg="#FF8C00", fg="white", **estilo_base, command=lambda: interagir("R")).place(x=60, y=200)
    tk.Button(janela_calc, text="I", bg="#1E90FF", fg="white", **estilo_base, command=lambda: interagir("I_URI")).place(x=145, y=200)

    tk.Button(janela_calc, text="P", bg="#FF4500", fg="white", **estilo_topo, command=lambda: interagir("P")).place(x=360, y=130)
    tk.Button(janela_calc, text="U", bg="#FFD700", fg="black", **estilo_base, command=lambda: interagir("U_PUI")).place(x=320, y=200)
    tk.Button(janela_calc, text="I", bg="#1E90FF", fg="white", **estilo_base, command=lambda: interagir("I_PUI")).place(x=405, y=200)

    tk.Label(janela_calc, text="Clique na grandeza que deseja descobrir", bg="#2c3e50", fg="#FFFFFF", font=("Arial", 10)).place(x=160, y=330)

def gerar_orcamento():  # Gera o orçamento em PDF
    janela.iconify()

    valor_hora = simpledialog.askfloat("Mecanicar", "Digite o seu valor/hora:")
    if valor_hora is None: return
    tempo = simpledialog.askfloat("MecaniCar", "Digite o valor do tempo gasto no serviço (horas):")
    if tempo is None: return
    custo_peca = simpledialog.askfloat("MecaniCar", "Digite o valor total das peças:")
    if custo_peca is None: return
    nome_mecanico = simpledialog.askstring("MecaniCar", "Digite o nome do mecânico responsável:")
    if nome_mecanico is None: return
    nome_cliente = simpledialog.askstring("MecaniCar","Digite o nome do cliente:")
    if nome_cliente is None: return
    observacoes = simpledialog.askstring("MecaniCar", "Digite as observações (opcional):")
    if observacoes is None: 
        janela.deiconify()
        return

    mao_de_obra = tempo * valor_hora
    valor_pecas = custo_peca * 1.3
    taxa_insumos = mao_de_obra * 0.05
    resultado = mao_de_obra + valor_pecas + taxa_insumos

    pdf = FPDF()
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "MECANICAR - ORÇAMENTO DE SERVIÇO", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(100, 10, f"CLIENTE: {nome_cliente.upper()}", ln=0)
    pdf.cell(100, 10, f"MECÂNICO: {nome_mecanico.upper()}", ln=1)
    pdf.ln(5)

    pdf.set_font("Arial", "", 12)
    pdf.cell(140, 10, "Mão de Obra", 1)
    pdf.cell(50, 10, f"R$ {mao_de_obra:.2f}", 1, 1, 'R')
    
    pdf.cell(140, 10, "Peças", 1)
    pdf.cell(50, 10, f"R$ {valor_pecas:.2f}", 1, 1, 'R')
    
    pdf.cell(140, 10, "Insumos e Materiais", 1)
    pdf.cell(50, 10, f"R$ {taxa_insumos:.2f}", 1, 1, 'R')

    pdf.set_font("Arial", "B", 12)
    pdf.cell(140, 10, "VALOR TOTAL", 1)
    pdf.cell(50, 10, f"R$ {resultado:.2f}", 1, 1, 'R')

    if observacoes: 
        pdf.ln(5) 
        pdf.set_font("Arial", "B", 11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, "OBSERVAÇÕES:", 0, 1) # Título da seção
        pdf.multi_cell(0, 6, observacoes, 1)

    pdf.set_y(-45)

    
    pdf.set_font("Arial", "I", 10)

    x_inicial = 20
    y_atual = pdf.get_y()
    pdf.line(x_inicial, y_atual, x_inicial + 80, y_atual) 

    pdf.set_xy(x_inicial, y_atual + 2)
    pdf.cell(80, 10, f"Assinatura do cliente: {nome_cliente.upper()}", 0, 0, 'C')

    x_mecanico = 110
    pdf.line(x_mecanico, y_atual, x_mecanico + 80, y_atual)

    pdf.set_xy(x_mecanico, y_atual + 2)
    pdf.cell(80, 10, f"Assinatura do mecânico: {nome_mecanico.upper()}", 0, 0, 'C')

    agora = datetime.now()
    data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")

    pdf.set_y(-25)
    pdf.cell(0, 10, f"Documento gerado em: {data_hora} | Feito com o MecaniCar", 0, 0, 'C')

    nome_arquivo = f"Orcamento_{nome_cliente.replace(' ', '_')}.pdf"
    pdf.output(nome_arquivo)
    
    os.startfile(nome_arquivo)

    messagebox.showinfo("Sucesso", f"Orçamento de R${resultado:.2f} gerado para {nome_cliente}!")
    
def bateria_repouso():  # Calcula a bateria em repouso
    tensao_bateria = simpledialog.askfloat("Mecanicar", "Digite aqui a tensão da bateria em repouso (V):", minvalue=0.1, maxvalue=13.0)

    if tensao_bateria is None:
        return

    carga_bateria = "Carga Crítica"
    msg_tipo = messagebox.showwarning

    if tensao_bateria >= 12.6:
        carga_bateria = "Carga da bateria: 100%"
        msg_tipo = messagebox.showinfo
    elif 12.4 <= tensao_bateria < 12.6:
        carga_bateria = "Carga da bateria: 75%"
        msg_tipo = messagebox.showinfo
    elif 12.2 <= tensao_bateria < 12.4:
        carga_bateria = "Carga da bateria: 50%"
        msg_tipo = messagebox.showinfo
    elif 12.0 <= tensao_bateria < 12.2:
        carga_bateria = "Carga da bateria: 25%"
        msg_tipo = messagebox.showwarning
    elif tensao_bateria < 12.0:
        carga_bateria = "Carga da bateria: abaixo de 20%"
        msg_tipo = messagebox.showwarning

    msg_tipo("Diagnóstico MecaniCar", f"""
        Resultados do Teste:
        -------------------------------------------
        Tensão da bateria: {tensao_bateria:.1f}V
        {carga_bateria}
        """)
    
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

        dados_para_simular = {
            "resistores": valores,
            "tensao": tensao,
            "corrente": corrente,
            "req": req
        }

        janela_calculo.destroy()

        simulador = SimuladorGrafico(dados_para_simular)
        simulador.iniciar()

    except Exception as e:
        messagebox.showerror("Erro", "Verifique os valores inseridos.")
    
def calcular_paralelo_logica(entradas, janela_calculo, tensao): # Calcula circuito paralelo
    try:
        valores = [float(en.get().replace(',', '.')) for en in entradas if en.get()]
        if not valores: return
        
        soma_inversos = sum(1/r for r in valores if r > 0)
        req_paralelo = 1 / soma_inversos
        corrente = tensao / req_paralelo
        potencia = (tensao ** 2) / req_paralelo

        # Organizamos os dados para a classe SimuladorParalelo
        dados_para_simular = {
            "resistores": valores,
            "tensao": tensao,
            "corrente": corrente,
            "req": req_paralelo,
            "potencia": potencia
        }

        janela_calculo.destroy() # Fecha a janela de entrada de dados

        # CHAMA A ANIMAÇÃO PARALELA
        simulador = SimuladorParalelo(dados_para_simular)
        simulador.iniciar()

    except ZeroDivisionError:
        messagebox.showerror("Erro", "Resistência não pode ser zero!")
    except Exception as e:
        messagebox.showerror("Erro", f"Preencha corretamente: {e}")

def abrir_github(): # Abre o Github através do botão
    webbrowser.open("https://github.com/Ozuhtra/MecaniCar")

def abrir_janela_serie():   # Abre a janela p/ calcular o paralelo
    configurar_janela(calcular_dinamico, "Série")

def abrir_janela_paralelo():    # Abre a janela p/ calcular o série
    configurar_janela(calcular_paralelo_logica, "Paralelo")

def configurar_janela(funcao_calculo, tipo):    # Configurações da janela
    try:
        # Criamos uma janela oculta temporária para segurar o foco
        janela.withdraw() 
        
        tensao = simpledialog.askfloat("MecaniCar", "Tensão do sistema (V):", minvalue=0.1)
        if tensao is None: 
            janela.deiconify()
            return
            
        num_res = simpledialog.askinteger("MecaniCar", "Quantos resistores?", minvalue=1)
        if num_res is None: 
            janela.deiconify()
            return

        janela.deiconify() # Traz a principal de volta
        
        nova_janela = tk.Toplevel(janela)
        nova_janela.title(f"Entrada {tipo}")
        # FORÇA A JANELA PARA A FRENTE
        nova_janela.attributes('-topmost', True) 
        
        entradas = []
        for i in range(num_res):
            tk.Label(nova_janela, text=f"Resistor {i+1} (Ω):").pack(pady=2)
            en = tk.Entry(nova_janela)
            en.pack(pady=2)
            entradas.append(en)

        tk.Button(nova_janela, text="CALCULAR", bg="blue", fg="white", font=("Arial", 15, "bold"),
                  command=lambda: funcao_calculo(entradas, nova_janela, tensao)).pack(pady=10)
    except Exception as e:
        janela.deiconify()
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

# ----- BOTÕES -----
frame_calculadoras = tk.Frame(janela, bg="#061824") # Use a cor do seu fundo ou mantenha transparente
frame_calculadoras.place(relx=0.09, rely=0.5, anchor="center")

# Frame para os conversores (Lado Direito)
frame_conversores = tk.Frame(janela, bg="#061824")
frame_conversores.place(relx=0.92, rely=0.5, anchor="center")

btn_triangulo_formulas = tk.Button(frame_conversores, text="Calcular lei de ohm",
                                    command=triangulo_formulas,
                                    width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"),
                                    relief="flat", borderwidth=0)
btn_triangulo_formulas.pack(pady=8)

btn_gerar_orcamento = tk.Button(frame_calculadoras, text="Gerar orçamento",
                                command=gerar_orcamento,
                                width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"),
                                relief="flat", borderwidth=0)
btn_gerar_orcamento.pack(pady=8)

btn_iniciar_serie = tk.Button(frame_calculadoras, text="Calcular circuito em série", 
                        command=abrir_janela_serie, 
                        width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"),
                        relief="flat", borderwidth=0)
btn_iniciar_serie.pack(pady=8)

btn_iniciar_paralelo = tk.Button(frame_calculadoras, text="Calcular circuito em paralelo", 
                        command=abrir_janela_paralelo, 
                        width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"),
                        relief="flat", borderwidth=0)
btn_iniciar_paralelo.pack(pady=8)

btn_calcular_cabo = tk.Button(frame_calculadoras, text="Calcular resistividade do cabo", 
                              command=resistencia_cabo,
                              width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"),
                              relief="flat", borderwidth=0)
btn_calcular_cabo.pack(pady=8)

btn_calcular_bateria = tk.Button(frame_calculadoras, text="Calcular a carga da bateria",
                                 command=bateria_repouso,
                                 width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"),
                                 relief="flat", borderwidth=0)
btn_calcular_bateria.pack(pady=8)

btn_calcular_temperatura = tk.Button(frame_conversores, text="Calcular temperatura",
                                     command=conversor_temperatura,
                                     width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"),
                                     relief="flat", borderwidth=0)
btn_calcular_temperatura.pack(pady=8)

btn_calcular_forca = tk.Button(frame_conversores, text="Calcular força",
                               command=conversor_forca,
                               width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"),
                               relief="flat", borderwidth=0)
btn_calcular_forca.pack(pady=8)

btn_calcular_potencia = tk.Button(frame_conversores, text="Calcular potência",
                               command=conversor_potencia,
                               width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"),
                               relief="flat", borderwidth=0)
btn_calcular_potencia.pack(pady=8)

btn_calcular_pressao = tk.Button(frame_conversores, text="Calcular pressão", 
                                 command=conversor_pressao,
                                 width=25, height=2, bg="#061824", fg="white", font=("Arial", 12, "bold"),
                                 relief="flat", borderwidth=0)
btn_calcular_pressao.pack(pady=8)

btn_versao_app = tk.Button(janela, text="v.0.0.5b",
                           command=abrir_github,
                           fg="red", font=("Arial", 12, "bold"),
                           relief="flat", borderwidth=0)
btn_versao_app.place(relx=0.95, rely=0.95, anchor="w")

btn_sair = tk.Button(janela, text="Fechar", command=fechar_janela, 
                     fg="white", bg="#800000", font=("Arial", 10, "bold"),
                     width=10, relief="flat", borderwidth=0)
btn_sair.place(relx=0.5, rely=0.92, anchor="center")

def sobre_eu():
    messagebox.showinfo("Pedro Michelin", "Sou o Pedro, amante de carros, eletroeletrônica, programação e futuro Engenheiro Elétrico!.")

def sobre_olavo():
    messagebox.showinfo("Pedro Henrique", "Sou o Pedro, amante de matemática, programação e futuro Engenheiro Mecânico!")

btn_sobre_eu = tk.Button(janela, text="Sobre o Pedro Michelin", command=sobre_eu, fg="blue")
btn_sobre_eu.place(relx=0.43, rely=0.956, anchor="center")

btn_sobre_olavo = tk.Button(janela, text="Sobre o Pedro Henrique", command=sobre_olavo, fg="pink")
btn_sobre_olavo.place(relx=0.57, rely=0.956, anchor="center")

janela.mainloop()