#desenvolvido por Gabriel Lavareda, LikedIn: https://www.linkedin.com/in/gabriellavareda/

#Importando Bibliotecas Necessárias, verifique o PIP FREEZE em READ-ME
import pyautogui as auto
import keyboard as keyb
import pyperclip
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import re

# Essa parte serve para obter o caminho do arquivo "caminho.txt", este arquivo 
# conterá o endereço da pasta "padrão" de "salvamento" quando utilizado o ALT + S
script_dir = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(script_dir, 'caminho.txt')

#função para a leitura do caminho padrão
def read_path():
    with open(caminho_arquivo, 'r') as arquivo:
        caminho_padrao = arquivo.read()
        return caminho_padrao

#Função Tkinter, serve para obter o caminho desejado quando utilizado o comando ALT + A
def selecionar_diretorio():
    root = tk.Tk()
    root.withdraw()  
    caminho = filedialog.askdirectory() 
    return caminho

#Alertas de Retorno para o Usuário (Tkiter)
def show_alert_padrao(caminho):
    messagebox.showinfo("HotkeyVideoDownloader", f"Baixado com Sucesso\n Local:\n {caminho}")

def show_alert_proibido():
    messagebox.showwarning(f"HotkeyVideoDownloader", "Esse vídeo NÃO pode ser baixado!"
                           f"\nPossível motivo: Vídeo somente para membros!")
def show_alert_error():
    messagebox.showwarning("HotkeyVideoDownloader", "Ocorreu um Erro")

def url_invalida():
    messagebox.showwarning("HotkeyVideoDownloader", "URL Inválida!")

def url_exit():
    messagebox.showwarning("HotkeyVideoDownloader", "Finalizando Tarefa...")

#Função para baixar vídeos das redes sociais (facebook e twitter), utilizando a fork yt-dlp
def download_video(url, output_path):
    try:
        result = subprocess.run(
            ['yt-dlp', '-o', f'{output_path}/%(title)s.%(ext)s', url],
            check=True,
            capture_output=True,
            text=True
        )
        show_alert()
    
    except subprocess.CalledProcessError as e:
        show_alert_error()

# Para que o código funcione de acordo devemos padronizar o url do twitter para que a tentative do download seja feito apenas
# quando um vídeo ou alguma publicação estiver aberta.
def padronizar_url(url):
    # Removendo a parte entre 'https://x.com/' e '/status/' e qualquer texto após '/status/'
    url_normalizada = re.sub(r'https://x.com/[^/]+/status/\d+', 'https://x.com//status/', url)
    return url_normalizada

# Essa parte do código é semelhante com a de cima, a diferença é que os URLS do Facebook e Youtube são semelhantes onde
# o código do vídeo ficam ao final, já no twitter, fica no meio.

# o Código abaixo seleciona apenas os primeiros 30 caracteres do link para verificar se são validos ou não.
def get_url():
    auto.hotkey("altleft", "d")
    auto.hotkey("ctrlleft", "c")
    url_alvo = pyperclip.paste()
    auto.press("esc")
    url_check = url_alvo[:30]
    return url_check, url_alvo

while True:
#configurar pasta padrao
    if keyb.is_pressed("alt") and keyb.is_pressed("m"):
        novo_diretorio_padrao = selecionar_diretorio()
        with open(caminho_arquivo, 'w') as arquivo:
            arquivo.write(novo_diretorio_padrao)
        


# salvar automaticamente
    if keyb.is_pressed("alt") and keyb.is_pressed("s"):
        url_check, url_alvo = get_url()
        check_twitter = padronizar_url(url_alvo)
        caminho_padrao = read_path()

        if url_check == ("https://www.youtube.com/watch?") or url_check == ("https://www.youtube.com/shorts"):
            try:
                yt = YouTube(url_alvo)
                stream = yt.streams.get_highest_resolution()
                stream.download(output_path=caminho_padrao)
                show_alert_padrao(caminho_padrao)

            except VideoUnavailable:
                show_alert_proibido()
            
            except Exception as e:
                show_alert_error()

        elif url_check == ("https://www.facebook.com/watch") or url_check == ("https://www.facebook.com/reel/"):
            facebookdownurl = url_alvo
            download_video(facebookdownurl, caminho_padrao)

        elif check_twitter == "https://x.com//status/":
            twitterdownurl = url_alvo
            download_video(twitterdownurl, caminho_padrao)

        else:
            url_invalida()

# escolher pasta e salvar
    elif keyb.is_pressed("alt") and keyb.is_pressed("a"):
        url_check, url_alvo = get_url()
        check_twitter = padronizar_url(url_alvo)

        if url_check == ("https://www.youtube.com/watch?") or url_check == ("https://www.youtube.com/shorts"):
            try:
                caminho_selecionado = selecionar_diretorio()
                yt = YouTube(url_alvo)
                stream = yt.streams.get_highest_resolution()
                stream.download(output_path=caminho_selecionado)
                show_alert_padrao(caminho_selecionado)

            except VideoUnavailable:
                show_alert_proibido()
            
            except Exception as e:
                show_alert_error()
            
        elif url_check == ("https://www.facebook.com/watch") or url_check == ("https://www.facebook.com/reel/"):
            caminho_selecionado = selecionar_diretorio()
            facebookdownurl = url_alvo
            download_video(facebookdownurl, caminho_selecionado)

        elif check_twitter == "https://x.com//status/":
            caminho_selecionado = selecionar_diretorio()
            twitterdownurl = url_alvo
            download_video(twitterdownurl, caminho_selecionado)

        else:
            url_invalida()
            
#encerrar programa
    elif keyb.is_pressed("alt") and keyb.is_pressed("c"):
        url_exit()
        quit()


