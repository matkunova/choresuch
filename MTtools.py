def parseCmd(line, lineNo=0):
    s = line.split('->')
    q0,c0 = s[0].split(',')
    q1,c1,M = s[1].split(',')
    return q0,c0,q1,c1,M

def parse(text):
    prog = {}
    for n,l in enumerate(text.split('\n')):
        q0,c0,q1,c1,M = parseCmd(l,n+1)
        prog[q0,c0] = q1,c1,M
    return prog    

P = """q1,1->q2,0,L
q2,0->q2,0,L
q1,0->q3,1,R
q2,1->q3,0,L
q3,1->q4,0,N
q4,0->q2,0,R
q4,1->q0,0,N"""
print(parse(P))
print(parseCmd('q1,1->q2,0,L'))


    
