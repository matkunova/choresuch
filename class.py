from tkinter import *


class Block(LabelFrame):
    def __init__(self, master=None, **kwargs):
        LabelFrame.__init__(self, master, **kwargs)
        self.K = Button(self, text="text")
        self.K.grid(row=0, column=0, sticky='news')
        self.K.bind("<Button-1>", copytext)
        self.M = Label(self, text="another text")
        self.M.grid(row=0, column=1, sticky='news')
        self.V = StringVar()
        self.V.set('Введите хоть что-нибудь')
        self.M.bind("<Motion>", self.dump)
        self.E = Entry(self, textvariable = self.V)
        #self.E.insert(0, 'Введите хоть что-нибудь')
        self.E.grid(row=1, column=0, sticky='ew')
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        
    def dump(*args, **kwargs):
        print(args, kwargs)
        
class Program(Frame):
    def __init__(self, **kwargs):
        # Пускай конструктор Frame сделает с нашей рамочкой
        # всё, что полагается
        Frame.__init__(self, **kwargs)
        # Поуправляем toplevel окном
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        # Наше окно прилипает ко всем 4 сторонам, Света
        self.grid(row=0, column=0, sticky="news")
        # Надпись
        self.L = Label(self, text="что-то")
        self.L.grid(row=0, column=0, sticky='ew')
        # Кнопка выхода
        self.B = Button(self, text="Quit", command=self.master.quit)
        self.B.grid(row=0, column=1, sticky="nw")
        # Рамочка с другими виждетами внутри
        self.Bl = Block(self, text = "текст в LabelFrame")
        self.Bl.grid(row=1, column=0, columnspan=2, sticky='news')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        
def dump(*args, **kwargs):
    print(args, kwargs)

def copytext(event):
    P.Bl.M.configure(text=P.Bl.V.get()) 
    
P = Program()
P.mainloop()
P.master.destroy()
