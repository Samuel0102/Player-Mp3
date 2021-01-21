"""Este módulo representa a classe principal de um player MP3

Autor: Samuel Pacheco Ferreira

"""


import tkinter as tk
import tkinter.filedialog
import os
import pygame
from random import randint


class Application:
    """Esta classe representa a aplicação como um todo

    Args:
        root (object): refere-se a janela raíz, a principal
        last_musics (list): lista contendo as músicas ja reproduzidas
        SONG_END (constant): controlador do fim da música
        img_text_frame (object): conteiner dos widgets de imagem e texto
        buttons_frame (object): conteiner dos botões abaixo da imagem, para controle 

    """


    def __init__(self, root=None):
        """Método construtor e inicializador de outros métodos

        Args:
            root (object): refere-se a janela raíz, a principal
        """
        self.root = root

        self.root.title("MP3 PLAYER")

        self.last_musics = []

        self.SONG_END = pygame.USEREVENT + 1

        self.img_text_frame = tk.Frame(root)
        self.img_text_frame.grid()

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.grid(pady=10)

        self.create_img_text()
        self.create_player_buttons()
        self.create_listbox_button()

        self.init_pygame()

    def create_img_text(self):
        """Método responsável pela criação dos widgets de imagem/texto

        """
        self.photo = tk.PhotoImage(file="images\\fundo.png")
        self.back = tk.Label(self.img_text_frame, image=self.photo)
        self.back.grid(padx=20,pady=20)

        self.actual_music = tk.Label(self.img_text_frame, text="",
                                    font="15",height=2,width=57,
                                    borderwidth=2,relief="solid")
        self.actual_music.grid(row=1,column=0)

    def create_player_buttons(self):
        """Método responsável pela criação dos widgets dos botões utilitários

        """
        self.play = tk.PhotoImage(file="images\\play.png")
        self.prev = tk.PhotoImage(file="images\\previous.png")
        self.nex = tk.PhotoImage(file="images\\next.png")
        self.pause = tk.PhotoImage(file="images\\pause.png")

        self.but_nex = tk.Button(self.buttons_frame, image= self.nex, command=self.select_new_music)
        self.but_prev = tk.Button(self.buttons_frame, image=self.prev, command=self.select_previous_music)
        self.but_play= tk.Button(self.buttons_frame, image=self.play, command=self.unpause_music)
        self.but_pause = tk.Button(self.buttons_frame, image=self.pause, command=self.pause_music)

        self.but_nex.grid(row=2,column=3,padx=2)
        self.but_prev.grid(row=2,column=0,padx=2)
        self.but_play.grid(row=2,column=1)
        self.but_pause.grid(row=2,column=2,padx=2)

    def create_listbox_button(self):
        """Método responsável pelo widget contendo todas as músicas

        """
        self.list = tk.Listbox(self.root, height=20, width=40)

        self.but_directory = tk.Button(self.root,
                                    text="Adicionar Diretório", 
                                    font="15", command=self.load_directory)

        self.list.grid(row=0,column=1)
        self.but_directory.grid(row=1,column=1)

    def load_directory(self):
        """Método para carregar diretório com músicas

        """
        directory = tkinter.filedialog.askdirectory()
        os.chdir(directory)

        self.load_musics()

    def load_musics(self):
        """Método para ler todas as músicas do diretório

        Responsável, também, por adicionar à lista de músicas
        a tocar

        """
        if self.list.size() > 0:
            self.list.delete(0,tk.END)

        for pos, music in enumerate(os.listdir()):
            self.list.insert(pos, music)

    def select_new_music(self):
        """Método responsável por selecionar (aleatoriamente) próxima música

        """
        try:
            self.music = self.list.get(randint(0, self.list.size()-1))
        except:
            self.actual_music["text"] = "Nenhum diretório selecionado :C"
            return

        self.actual_music["text"] = self.music.replace(".mp3", "")

        self.load_music()

    def init_pygame(self):
        """Método responsável por inicializar componentes do pygame

        """
        pygame.init()
        pygame.mixer.init()

    def load_music(self):
        """Método para carregar dados da música selecionada

        """
        pygame.mixer_music.load(self.music)

        self.play_music()

    def play_music(self):
        """Método para reproduzir música selecionada

        Também responsável por adicionar a música tocada
        dentro da lista de já reproduzidas

        """
        pygame.mixer_music.play()
        self.last_musics.insert(0, self.music)

        pygame.mixer_music.set_endevent(self.SONG_END)
        
    def pause_music(self):
        """Método para pausar música

        """
        pygame.mixer_music.pause()

    def unpause_music(self):
        """Método para despausar música

        """
        pygame.mixer_music.unpause()

    def check_music(self):
        """Método para verificar se música chegou ao fim

        Utilizado para seleção automática de músicas
        sem necessitar do usuário clicar para pular

        """
        for event in pygame.event.get():
            if event.type == self.SONG_END:
                self.select_new_music()

    def select_previous_music(self):
        """Método para retornar a última música reproduzida

        Apenas retorna à última música, as penúltimas, antepenúltimas,
        etc., não serão reproduzidas

        """
        if len(self.last_musics) == 1:
            self.music = self.last_musics[0]
            
        elif len(self.last_musics) > 1:
            self.music = self.last_musics[1]

        self.actual_music["text"] = self.music.replace(".mp3", "")

        self.load_music()
        
        