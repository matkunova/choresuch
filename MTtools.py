#!/usr/bin/env python3

def parseCmd(line, lineNo=0):
    """ Из строки программы получает внутренее представление команды

    >>> print(parseCmd('q1,1->q2,0,L'))
    ('q1', '1', 'q2', '0', 'L')
    """

    line = line.strip()
    if line == '' or line.startswith("#"):
        return None, None, None, None, None
    s = line.split('->')
    q0,c0 = s[0].split(',')
    q1,c1,M = s[1].split(',')
    return q0.strip(),c0.strip()[0],q1.strip(),c1.strip()[0],M.strip()[0]

def parse(text):
    """ Из текста программы получает внутреннее представление программы

    >>> import pprint
    >>> P = '''q1,1->q2,0,L
    ... q2,0->q2,0,L
    ... q1,0->q3,1,R
    ... q2,1->q3,0,L
    ... q3,1->q4,0,N
    ... q4,0->q2,0,R
    ... q4,1->q0,0,N'''
    >>> program, log = parse(P)
    >>> pprint.pprint(program)
    {('q1', '0'): ('q3', '1', 'R'),
     ('q1', '1'): ('q2', '0', 'L'),
     ('q2', '0'): ('q2', '0', 'L'),
     ('q2', '1'): ('q3', '0', 'L'),
     ('q3', '1'): ('q4', '0', 'N'),
     ('q4', '0'): ('q2', '0', 'R'),
     ('q4', '1'): ('q0', '0', 'N')}
    """
    # TODO сохранять номер строки
    # TODO проверять повторное задание состояния
    
    log = []
    prog = {}
    for n,l in enumerate(text.split('\n')):
        try:
            q0,c0,q1,c1,M = parseCmd(l,n+1)
            if q0:
                prog[q0,c0] = q1,c1,M
        except Exception:
            log.append(f"Ошибка в строке {n}: '{l}'")
    return prog, "\n".join(log)

class RW:
    """Считывающее устройство Машины Тьюринга

    >>> print(RW())
    [_]
    """
    band = ''
    nulsb = '_'
    pos = 0
    initial = ''
    
    def __init__(self, nulsb = '_', pos = 0):
        self.nulsb = nulsb
        self.setword(nulsb)
        self.pos = pos # проверить

    def getsb(self):
        return self.band[self.pos]

    def setword(self, word):
        """ Устанавливает значение слова
        >>> a = RW()
        >>> a.setword("blabla")
        >>> print(a)
        [b]labla
        >>> a.move('R'); a.move('R'); a.move('R')
        >>> a.getsb()
        'b'
        >>> a.setword("ef")
        >>> a.getsb()
        'f'
        """
        if not word:
            word = self.nulsb
        if len(word) <= self.pos:
            self.pos = len(word)-1
            
        self.band = self.initial = word
        

    def setsb(self, sb):
        """ Устанавливает значение символа
        >>> a = RW()
        >>> a.setsb('b')
        >>> print(a)
        [b]
        """
        self.band = self.band[:self.pos]+sb+self.band[self.pos+1:]

    def __str__(self):
        return f"{self.band[:self.pos]}[{self.band[self.pos]}]{self.band[self.pos+1:]}"

    def move(self, direction):
        """ Сдвигает каретку на шаг вправо или влево
        >>> a = RW()
        >>> a.setword('blabla')
        >>> a.move('R')
        >>> print(a.pos)
        1
        >>> a.move('L')
        >>> a.move('L')
        >>> print(a.pos)
        0
        >>> print(a)
        [_]blabla
        >>> b = RW()
        >>> b.setword('j')
        >>> b.move('R')
        >>> print(b)
        j[_]
        >>> print(b.pos)
        1
        >>> b.move('L')
        >>> a.move('R')
        >>> print(a, b)
        [b]labla [j]
        """
        
        if direction == 'L':
            if self.pos > 0:
                self.pos -= 1
            else:
                self.band = self.nulsb + self.band
        elif direction == 'R':
            self.pos += 1
            if self.pos >= len(self.band)-1:
                self.band = self.band + self.nulsb
        if self.pos > 0 and self.band[0] == self.nulsb:
            self.pos, self.band = self.pos-1, self.band[1:]
        if self.pos < len(self.band)-1 and self.band[-1] == self.nulsb:
            self.band = self.band[:-1]

class MT:
    """ Класс, реализующий Машину Тьюринга

    >>> program, log = parse('''q1,1->q1,1,R
    ... q1,_->q0,0,N''')
    >>> mt = MT('111', program)
    >>> print(mt)
    [1]11, 0, q1
    >>> mt.step()
    >>> print(mt)
    1[1]1, 1, q1
    >>> mt.step()
    >>> print(mt)
    11[1], 2, q1
    >>> mt.step()
    >>> print(mt)
    111[_], 3, q1
    >>> mt.step()
    >>> print(mt)
    111[0], 3, q0
    >>> mt.step()
    Traceback (most recent call last):
      File "<pyshell#52>", line 1, in <module>
        mt.step()
      File "/home/pauline/Полина/Desktop/Полиныч/матфак/3 курс/2 семестр/курсач/MTtools.py", line 138, in step
        raise StopIteration
    StopIteration
    """
    qB = 'q1'
    qC = 'q1'
    qE = 'q0'
    ipos = 0
    rw = None
    prog = {}

    def __init__(self, w, prog, qB='q1', qE='q0', nulsb='_', pos=0):
        self.qB = qB
        self.qE = qE
        self.qC = qB
        self.prog = prog
        self.ipos = pos
        self.rw = RW(nulsb, pos)
        self.rw.setword(w)

    def step(self):
        if self.qC == self.qE:
            raise StopIteration
        qT, sb, D = self.prog[self.qC, self.rw.getsb()]
        self.rw.setsb(sb)
        self.rw.move(D)
        self.qC = qT

    def __str__(self):
        return f'{self.rw}, {self.rw.pos}, {self.qC}'

    def alphabet(self):
        """ Алфавит Машины Тьюринга
        >>> program, log = parse('''q1,1->q1,1,R
        ... q1,_->q0,0,N''')
        >>> mt = MT('112', program)
        >>> mt.alphabet()
        ['0', '1', '2', '_']
        """
        aW = set(self.rw.band)
        aL = {c for q,c in self.prog}
        aR = {c for q,c,m in self.prog.values()}
        return sorted((aW|aL|aR)-{self.rw.nulsb})+[self.rw.nulsb]

    def states(self):
        """
        >>> program, log = parse('''q1,1->q1,1,R
        ... q1,_->q0,0,N''')
        >>> mt = MT('112', program)
        >>> mt.states()
        ['q1', 'q0']
        """
        sL = {q for q,c in self.prog}
        sR = {q for q,c,m in self.prog.values()}
        return [self.qB]+sorted((sL|sR)-{self.qE, self.qB})+[self.qE]

    def reset(self):
        self.rw.pos = self.ipos
        self.rw.setword(self.rw.initial)
        self.qC = self.qB
        
        
if __name__ == "__main__":
    # TODO Argparse
    import sys
    from pprint import pprint
   
    if len(sys.argv)<2:
        print(f"Запуск: {sys.argv[0]} программа.mt [входное_слово [начальное положение]]", file=sys.stderr)
        sys.exit(0)
    f = open(sys.argv[1])
    word = sys.argv[2] if len(sys.argv)>2 else input('Входное слово: ')
    pos = int(sys.argv[3]) if len(sys.argv)>3 else 0
    debug = len(sys.argv)>3 # очень временный костыль
      
    P, log = parse(f.read())
    f.close()
    print(log)
    qB = list(P.keys())[0][0]
    m = MT(word, P, qB=qB, pos=pos)
    if debug:
        pprint(P)
    cont = ""
    while m.qC != m.qE:
        if debug:
            print('\t',m)
            if not cont:
                cont = input("> ")
        m.step()
    print(m.rw.band)
