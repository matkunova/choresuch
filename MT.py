#!/usr/bin/env python3
from tkinter import *

class Word(LabelFrame):
    def __init__(self, master=None, **kwards):
        LabelFrame.__init__(self, master, kwards)
        self.V = StringVar()
        self.V.set('')
        self.E = Entry(self, textvariable = self.V)
        self.E.grid(row=0, column=0, sticky='ew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)

class ButCtrl(LabelFrame):
    def __init__(self, master=None, **kwards):
        LabelFrame.__init__(self, master, kwards)
        self.B = Button(self, text="Запустить")
        self.B.grid(row=0, column=0, sticky="nw")
        self.F = Button(self, text="Шаг вперёд")
        self.F.grid(row=0, column=1, sticky="nw")
        self.Bk = Button(self, text="Шаг назад")
        self.Bk.grid(row=0, column=2, sticky="nw")
        self.S = Button(self, text="Стоп")
        self.S.grid(row=0, column=3, sticky="nw")
        self.Bg = Button(self, text="В начало")
        self.Bg.grid(row=0, column=4, sticky="nw")
        self.C = Button(self, text="Очистить")
        self.C.grid(row=0, column=5, sticky="nw")

class Pr(LabelFrame):
    def __init__(self, master=None, **kwards):
        LabelFrame.__init__(self, master, kwards)
        self.V = StringVar()
        self.V.set('Текст программы')
        self.E = Entry(self, textvariable = self.V)
        self.E.grid(row=0, column=0, sticky='news')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

class Table(LabelFrame):
    def __init__(self, master=None, **kwards):
        LabelFrame.__init__(self, master, kwards)
        self.L = Label(self, text='Здесь будет таблица')
        self.L.grid(row=0, column=0, sticky='news')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

class Journal(LabelFrame):
    def __init__(self, master=None, **kwards):
        LabelFrame.__init__(self, master, kwards)
        self.J = Label(self, text='Это события')
        self.J.grid(row=0, column=0, sticky='news')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

class Program(Frame):
    def __init__(self, **kwards):
        Frame.__init__(self, **kwards)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky='news')
        self.W = Word(self, text = "Слово")
        self.W.grid(row=0, column=0, columnspan=2, sticky='ew')
        self.B = ButCtrl(self, text = "Управление кнопками")
        self.B.grid(row=1, column=0, columnspan=2)
        self.Tp = Pr(self, text = "Текст программы")
        self.Tp.grid(row=2, column=0,rowspan=2, sticky='news')
        self.T = Table(self, text='таблица')
        self.T.grid(row=2, column=1, sticky='news')
        self.J = Journal(self, text = "Журнал")
        self.J.grid(row=3, column=1, sticky='news')
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

P = Program()
P.mainloop()
P.master.destroy()
