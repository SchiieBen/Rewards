import pyautogui as pg
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import keyboard
import os
import pygetwindow as gw

def monitorar_tecla(event):
    if event.name == "esc":
        pg.moveTo(0, 0)
        sys.exit()

keyboard.on_press_key("esc", monitorar_tecla)

def confirmar(event=None):
    global data
    data = Resposta.get().strip().lower()
    Janela.after(3000, lambda: Janela.destroy())
    dias_validos = [
        "segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo",
        "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira",
        "segunda feira", "terça feira", "quarta feira", "quinta feira", "sexta feira", "sabado",
        "seg", "ter", "qua", "qui", "sex", "sab", "dom",]
    dias_validos += [dia.capitalize() for dia in dias_validos]
    if data not in dias_validos:
        mostrar_erro()
        sys.exit()
    else:
        mostrar_confirmacao()

def mostrar_erro():
    messagebox.showerror("Erro", "Dia da semana inválido, tente de outra forma")

def mostrar_confirmacao():
    messagebox.showinfo("Confirmação", f"Dia da semana '{data}' confirmado!")

def Topicos_rewards():
    coordenadas = [
        (334, 767),
        (740, 767),
        (1000, 767)
    ]
    if keyboard.is_pressed('esc'):
        sys.exit()
    pg.write("https://rewards.bing.com/")
    time.sleep(0.5)
    pg.press("enter")
    time.sleep(2)
    for x, y in coordenadas:
        if keyboard.is_pressed('esc'):
                sys.exit()
        pg.moveTo(x, y, duration=0.2)
        pg.sleep(0.3)
        pg.click()
        time.sleep(1.5)
        pg.hotkey("ctrl", "w")
        pg.sleep(1)
    procurar_e_scrollar()

def fechar_janela():
    sys.exit()

def iniciar_movimento(event):
    global x, y
    x, y = event.x, event.y

def mover_janela(event):
    nova_pos_x = Janela.winfo_pointerx() - x
    nova_pos_y = Janela.winfo_pointery() - y
    Janela.geometry(f"+{nova_pos_x}+{nova_pos_y}")

def verificar_janela_maximizada():
    janelas = gw.getAllWindows()
    janelas_opera = [janela for janela in janelas if 'Opera' in janela.title or 'Chrome' in janela.title]
    if janelas_opera:
        janela_opera = janelas_opera[0]
        if not janela_opera.isMaximized:
            janela_opera.maximize()

if os.path.exists(os.path.join(os.path.expanduser('~'), 'Documentos')):
    diretorio_executavel = os.path.join(os.path.expanduser('~'), 'Documentos', 'Rewards')
else:
    diretorio_executavel = os.path.join(os.path.expanduser('~'), 'Documents', 'Rewards')

imagens_procuradas = [
    os.path.join(diretorio_executavel, 'image1.png'),
    os.path.join(diretorio_executavel, 'image2.png')
]

def clicar_na_imagem(posicao_imagem):
    centro = pg.center(posicao_imagem)
    pg.moveTo(centro)
    time.sleep(0.2)
    pg.click() 
    time.sleep(1)
    pg.hotkey("ctrl", "w")
    time.sleep(0.2)

def procurar_e_scrollar():
    tentativas = 0
    max_tentativas = 6
    while tentativas < max_tentativas:
        try:
            if keyboard.is_pressed('esc'):
                sys.exit()
            pg.scroll(-350)
            time.sleep(1.5)
            tentativas += 1
            for imagem in imagens_procuradas:
                time.sleep(0.5)
                encontrado = pg.locateOnScreen(imagem, confidence=0.8)
                if encontrado:
                    time.sleep(0.2)
                    if keyboard.is_pressed('esc'):
                        sys.exit()
                    clicar_na_imagem(encontrado)
                    tentativas = 0
                    break
        except Exception as e:
            pass

# # # # # # # # #-----------Janela

Janela = tk.Tk()
Janela.title("Coleta de Dados")

style = ttk.Style(Janela)
Janela.attributes("-topmost", True)

tcl_dir = os.path.join(os.path.dirname(sys.executable), "tcl")
azure_path = os.path.join(tcl_dir, "azure.tcl")
Janela.attributes("-alpha", 0.9)
Janela.tk.call("source", azure_path)
Janela.tk.call("set_theme", "dark")

Janela.geometry(f"{430}x{185}+{430}+{280}")
Janela.overrideredirect(True)

title_bar = ttk.Frame(Janela, style='TFrame')
title_bar.pack(side='top', fill='x')
titulo = ttk.Label(title_bar, text="Coleta de Dados")
titulo.pack(side='left', padx=10)

botao_fechar = ttk.Button(title_bar, text='X', command=fechar_janela, width=5)
botao_fechar.pack(side='right', padx=(0, 10))

title_bar.bind('<ButtonPress-1>', iniciar_movimento)
title_bar.bind('<B1-Motion>', mover_janela)

Pergunta = ttk.Label(Janela, text="Digite o dia da semana atual:")
Pergunta.pack(pady=10)

Resposta = ttk.Entry(Janela, font=("Arial", 12), width=30)
Resposta.pack(pady=10)
Resposta.bind('<Return>', confirmar)

botao_navegador = ttk.Button(Janela)
botao_navegador = ttk.Label(Janela, text="chrome")

def alternar_navegador():
    global navegador
    if navegador == "Opera":
        navegador = "Chrome"
    else:
        navegador = "Opera"
    botao_navegador.config(text=navegador)

navegador = "Opera"
botao_navegador = ttk.Button(Janela, text=navegador, command=alternar_navegador)
botao_navegador.pack(pady=10)

Janela.mainloop()

# # # # # # # --------------------------------------------------------------------------

pg.press('win')
time.sleep(0.2)
pg.write(navegador)
time.sleep(0.2)
pg.press("enter")
time.sleep(4)

verificar_janela_maximizada()
time.sleep(0.3)
if navegador == "Chrome":
    pg.hotkey("ctrl", "t")
time.sleep(1)
Topicos_rewards() 
time.sleep(3)
if navegador == "Opera":
    pg.hotkey("ctrl", "w")

time.sleep(2)
pg.hotkey("ctrl", "t")
time.sleep(0.5)
if navegador == "Chrome":
    pg.hotkey("ctrl", "shift", "tab")
    time.sleep(0.3)
    pg.hotkey("ctrl", "w")
time.sleep(0.5)
pg.write("https://www.bing.com/?cc=br")
time.sleep(0.5)
pg.press("enter")
time.sleep(2)

alfabeto = [chr(i) for i in range(ord('a'), ord('z')+1)]

base_dia = {
    "segunda": "", "segunda feira": "","seg": "","segunda-feira": "","sexta": "", "sexta feira": "", "sexta-feira": "", "sex": "",
    "terça": "2", "terça feira": "2", "ter": "2", "terça-feira":"2", "sabado": "2", "sab": "2",
    "quarta": "4", "quarta feira": "4", "qua":"4", "quarta-feira": "4", "domingo": "4", "dom": "4",
    "quinta": "6", "quinta feira": "6", "qui": "6", "quinta-feira": "6"
}

for letra in alfabeto:
    termo = letra + base_dia.get(data, "")
    pg.write(termo)
    pg.press("enter")
    time.sleep(6)
    if keyboard.is_pressed('esc'):
        sys.exit()
    if letra == "z":
        alfabeto = [chr(i) for i in range(ord('a'), ord('d')+1)]
        for letra2 in alfabeto:
            termo = letra2 + ("1" if data in ["segunda", "segunda feira","seg","segunda-feira","sexta","sexta feira","sex","sexta-feira"] else 
                              "3" if data in ["terça", "terça feira", "ter", "terça-feira", "sabado", "sab"] else 
                              "5" if data in ["quarta", "quarta feira", "qua", "quarta-feira", "domingo", "dom"] else
                              "7" if data in ["quinta", "quinta feira", "qui", "quinta-feira"] else "")
            pg.write(termo)
            pg.press("enter")
            time.sleep(6)
            if keyboard.is_pressed('esc'):
                sys.exit()
