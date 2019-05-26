#!/usr/bin/env python3

def parseCmd(line, lineNo=0):
    """ Из строки программы получает внутренее представление команды

    >>> print(parseCmd('q1,1->q2,0,L'))
    ('q1', '1', 'q2', '0', 'L')
    """
    s = line.split('->')
    q0,c0 = s[0].split(',')
    q1,c1,M = s[1].split(',')
    return q0,c0,q1,c1,M

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
    >>> program = parse(P)
    >>> pprint.pprint(program)
    {('q1', '0'): ('q3', '1', 'R'),
     ('q1', '1'): ('q2', '0', 'L'),
     ('q2', '0'): ('q2', '0', 'L'),
     ('q2', '1'): ('q3', '0', 'L'),
     ('q3', '1'): ('q4', '0', 'N'),
     ('q4', '0'): ('q2', '0', 'R'),
     ('q4', '1'): ('q0', '0', 'N')}
    """
    
    prog = {}
    for n,l in enumerate(text.split('\n')):
        q0,c0,q1,c1,M = parseCmd(l,n+1)
        prog[q0,c0] = q1,c1,M
    return prog

class RW:
    """Считывающее устройство Машины Тьюринга

    >>> print(RW())
    _
    """
    band = ''
    nulsb = '_'
    pos = 0
    
    def __init__(self, nulsb = '_'):
        self.nulsb = nulsb
        self.band = nulsb

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
        
        




