"""Este módulo representa o sistema de execucação da aplicação

Autor: Samuel Pacheco Ferreira
"""


from class_application import Application
import tkinter as tk
import pygame

#criação da janela principal
root= tk.Tk()

#criacao do sistema contido na janela principal
app = Application(root)

#loop de execucao com verificação constante
while True:
    app.check_music()
    root.update()




