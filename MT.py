#!/usr/bin/env python3
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from MTtools import MT, parse
from pprint import pprint
from tkinter.ttk import Combobox

def tag(s):
    return str(s).replace('.', ',').replace(' ', '…')

    
class Word(LabelFrame):
    def __init__(self, master=None, **kwargs):
        LabelFrame.__init__(self, master, **kwargs)        
        self.V = StringVar()
        self.V.set('')
        self.E = Entry(self, textvariable = self.V)
        self.E.bind("<KeyPress>", self.keyPressed)
        self.E.grid(row=0, column=0, sticky='ew')
         
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)

    def keyPressed(self, *args):
        if self.V.get() != self.master.MT.rw.band:
            self.master.MT.rw.setword(self.V.get())   
               

class ButCtrl(LabelFrame):
    def __init__(self, master=None, **kwargs):
        LabelFrame.__init__(self, master, **kwargs)
        self.P = Label(self, text = "начальное\nположение")
        self.P.grid(row=0, column=0, sticky='news')
        self.sp = Spinbox(self, from_=0, increment=1, width=3)
        self.sp.grid(row=0, column=1, sticky='ew')
        self.Q = Label(self, text = "начальное\nсостояние")
        self.Q.grid(row=0, column=2, sticky='news')
        self.q = Combobox(self, values = ['q1'], width=3)
        self.q.set('q1')
        self.q.grid(row=0, column=3, sticky='ew')
        self.I = IntVar(0)
        self.S = Checkbutton(self, text="Стоп", variable = self.I)        
        self.S.grid(row=0, column=4, sticky="news")
        self.B = Button(self, text="Выполнить", command = self.do)
        self.B.grid(row=0, column=5, sticky="nw")
        self.F = Button(self, text="Шаг вперёд", command = self.forward)
        self.F.grid(row=0, column=6, sticky="nw")
##        self.Bk = Button(self, text="Шаг назад")
##        self.Bk.grid(row=0, column=3, sticky="nw")        
        self.Bg = Button(self, text="В начало", command = self.reset)
        self.Bg.grid(row=0, column=7, sticky="nw")
        self.C = Button(self, text="Очистить", command = self.clean)
        self.C.grid(row=0, column=8, sticky="nw")

    def forward(self, show=True):
        try:
            self.master.MT.step()
        except StopIteration:
            self.master.J.append("Выполнение закончено")
        except KeyError:
            self.master.J.append(f"Нет правила <{self.master.MT.qC}, {self.master.MT.rw.getsb()}>")
        except Exception:
            self.master.J.append("Произошла НЕХ")
        else:
            self.master.W.V.set(str(self.master.MT.rw))
            self.master.T.markQC()
            if show: 
                self.master.J.append(str(self.master.MT))
            return True
        return False

    def do(self):
        self.I.set(0)
        while self.forward(show=False):
            if self.I.get():
                self.I.set(0)
                break
            
    def clean(self):
        self.master.W.V.set('')

    def reset(self):
        self.master.MT.reset()
        self.master.W.V.set(self.master.MT.rw.band)
        self.master.J.append("Установлено исходное состояние Машины Тьюринга "+str(self.master.MT))
        self.master.T.markQC()

    def setState(self, *args):
        print(args)

class PrCtrl(Frame):
    def loadFile(self):
        self.Fname = askopenfilename(filetypes=[('MT programs','*.mt'),
                                                ('All files','*.*')],
                                     title = "Выбрать файл")
        O = open(self.Fname)
        self.master.E.delete(1.0, END)
        self.master.E.insert(1.0, O.read())
        O.close()

    def saveFile(self):
        self.Fname = asksaveasfilename(filetypes=[('MT programs','*.mt'),
                                                ('All files','*.*')],
                                   title = "Сохранить файл")
        O = open(self.Fname, 'w')
        O.write(self.master.E.get(1.0, END))
        O.close()

    def Compile(self):
        self.master.Comp, log = parse(self.master.E.get(1.0, END))
        self.master.master.J.J.delete(1.0, END)
        self.master.master.J.append(log if log else "Компиляция прошла успешно")
        states = [qc[0] for qc in self.master.master.Tp.Comp.keys()]
        qFirst = states[0]
        qB = self.master.master.B.q.get()
        if qB not in states:
            self.master.master.B.q.set(qFirst)
            qB = qFirst
        self.master.master.MT = MT(self.master.master.W.V.get(), self.master.master.Tp.Comp, qB=qB)
        self.master.master.T.fill()
        self.master.master.T.markQC()
        self.master.master.B.q['values'] = self.master.master.MT.states()
        self.master.master.B.q.set(self.master.master.MT.qB)

    def Clean(self):
        self.master.E.delete(1.0, END)
        
    def __init__(self, master=None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.R = Button(self, text="Загрузить", command = self.loadFile)
        self.R.grid(row=0, column=0, sticky="nw")
        self.W = Button(self, text="Записать", command = self.saveFile)
        self.W.grid(row=0, column=1, sticky="nw")
        self.M = Button(self, text="Скомпилировать", command = self.Compile)
        self.M.grid(row=0, column=2, sticky="nw")
        self.C = Button(self, text="Очистить", command = self.Clean)
        self.C.grid(row=0, column=3, sticky="nw")

class Pr(LabelFrame):
    def __init__(self, master=None, **kwargs):
        LabelFrame.__init__(self, master, **kwargs)
        # self.V = StringVar()
        # self.V.set('Текст программы')
        self.B = PrCtrl(self)
        self.B.grid(row=0, column=0, sticky="ew")
        self.E = Text(self, width=20)
        self.E.grid(row=1, column=0, sticky='news')
        self.Comp = {}
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

class Table(LabelFrame):
    def __init__(self, master=None, **kwargs):
        LabelFrame.__init__(self, master, **kwargs)
        self.T = Text(self, wrap = 'none')
        self.T.grid(row=0, column=0, sticky='news')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def fill(self):
        widthS = max(len(q) for q in self.master.MT.states())
        #         c       d      _
        #  q1  q1,c,R  q1,d,R  q1,_,L
        # q12 q12,d,L
        self.f0 = "{:>"+str(widthS)+"} "
        self.fc = "{:^"+str(widthS+4)+"} "
        self.f3 = "{:>"+str(widthS)+"},{},{} "
        self.T.delete(1.0, END)
        self.T.insert(END, self.f0.format(" "))
        for c in self.master.MT.alphabet():
            self.T.insert(END, self.fc.format(c), tag(c))
        self.T.insert(END, '\n')
        for q in self.master.MT.states():
            self.T.insert(END, self.f0.format(q), tag(q))
            for c in self.master.MT.alphabet():
                if (q,c) in self.master.MT.prog:
                    self.T.insert(END, self.f3.format(*(self.master.MT.prog[q,c])), tag(q+c))
                else:
                    self.T.insert(END, self.f3.format(*"   "), tag(q+c))
            self.T.insert(END, '\n')        

    def markQC(self):
        self.T.tag_delete('char')
        self.T.tag_delete('state')
        self.T.tag_delete('rule')
        q,c = self.master.MT.qC, self.master.MT.rw.getsb()
        self.T.tag_add('char', f"{tag(c)}.first", f"{tag(c)}.last")
        self.T.tag_add('state', f"{tag(q)}.first", f"{tag(q)}.last")
        self.T.tag_add('rule', f"{tag(q+c)}.first", f"{tag(q+c)}.last")
        self.T.tag_config('char', background='navajo white')
        self.T.tag_config('state', background='navajo white')
        self.T.tag_config('rule', background='navajo white')

class Journal(LabelFrame):
    def __init__(self, master=None, **kwargs):
        LabelFrame.__init__(self, master, **kwargs)
        self.J = Text(self)
        self.J.grid(row=0, column=0, sticky='news')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def append(self, text):
        self.J["state"]=NORMAL
        self.J.insert(END, text+'\n')
        self.J.see(END)
        self.J["state"]=DISABLED

        

class Program(Frame):
    def __init__(self, **kwargs):
        Frame.__init__(self, **kwargs)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky='news')
        self.W = Word(self, text = "Слово")
        self.W.grid(row=0, column=0, columnspan=2, sticky='ew')
        self.B = ButCtrl(self, text = "Управление")
        self.B.grid(row=1, column=0, columnspan=2)
        self.Tp = Pr(self, text = "Текст программы")
        self.Tp.grid(row=2, column=0,rowspan=2, sticky='news')
        self.T = Table(self, text='таблица')
        self.T.grid(row=2, column=1, sticky='news')
        self.J = Journal(self, text = "Журнал")
        self.J.grid(row=3, column=1, sticky='news')
        self.MT = MT(self.W.V.get(), self.Tp.Comp) 
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

P = Program()
P.mainloop()
P.master.destroy()
