#!/usr/bin/env python3

def parseCmd(line, lineNo=0):
    """ Из строки программы получает внутренее представление команды

    >>> print(parseCmd('q1,1->q2,0,L'))
    ('q1', '1', 'q2', '0', 'L')
    """
    line = line.strip()
    if line == '':
        return None, None, None, None, None
    s = line.split('->')
    q0,c0 = s[0].split(',')
    q1,c1,M = s[1].split(',')
    return q0.strip(),c0.strip(),q1.strip(),c1.strip(),M.strip()

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
    log = ''
    prog = {}
    for n,l in enumerate(text.split('\n')):
        try:
            q0,c0,q1,c1,M = parseCmd(l,n+1)
            if q0:
                prog[q0,c0] = q1,c1,M
        except Exception:
            log += f"Ошибка в строке {n}: '{l}'"
    return prog, log

class RW:
    """Считывающее устройство Машины Тьюринга

    >>> print(RW())
    _
    """
    band = ''
    nulsb = '_'
    pos = 0
    
    def __init__(self, nulsb = '_', pos = 0):
        self.nulsb = nulsb
        self.band = nulsb
        self.pos = pos # проверить

    def getsb(self):
        return self.band[self.pos]

    def setword(self, word):
        """ Устанавливает значение слова
        >>> a = RW()
        >>> a.setword("blabla")
        >>> print(a)
        blabla
        """
        self.band = word

    def setsb(self, sb):
        """ Устанавливает значение символа
        >>> a = RW()
        >>> a.setsb('b')
        >>> print(a)
        b
        """
        self.band = self.band[:self.pos]+sb+self.band[self.pos+1:]

    def __str__(self):
        return self.band

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
        _blabla
        >>> b = RW()
        >>> b.setword('j')
        >>> b.move('R')
        >>> print(b)
        j_
        >>> print(b.pos)
        1
        >>> b.move('L')
        >>> a.move('R')
        >>> print(a, b)
        blabla j
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
    111, 0, q1
    >>> mt.step()
    >>> print(mt)
    111, 1, q1
    >>> mt.step()
    >>> print(mt)
    111, 2, q1
    >>> mt.step()
    >>> print(mt)
    111_, 3, q1
    >>> mt.step()
    >>> print(mt)
    1110, 3, q0
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
    rw = None
    prog = {}

    def __init__(self, w, prog, qB='q1', qE='q0', nulsb='_', pos=0):
        self.qB = qB
        self.qE = qE
        self.qC = qB
        self.prog = prog
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
        
        
if __name__ == "__main__":
    # TODO Argparse
    import sys
    from pprint import pprint
   
    f = open(sys.argv[1])
    if len(sys.argv)>2:
        word = sys.argv[2]
    else:
        word = input('Входное слово: ')
    debug = len(sys.argv)>3 # очень временный костыль
      
    P, log = parse(f.read())
    f.close()
    print(log)
    m = MT(word, P)
    if debug:
        pprint(P)
    while m.qC != m.qE:
        if debug:
            print(m)
            input("> ")
        m.step()
    print(m.rw)
    



