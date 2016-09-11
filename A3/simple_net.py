##Simple Bayes net
##
from bnet import *

#'0' '1' for false/true
a = Variable('A', ['0','1'])
b = Variable('B', ['0','1'])
c = Variable('C', ['0','1'])
d = Variable('D', ['0','1'])
e = Variable('E', ['0','1'])
f = Variable('F', ['0','1'])
g = Variable('F', ['0','1'])
h = Variable('H', ['0','1'])
i = Variable('I', ['0','1'])

F1 = Factor("P(A)", [a])
F2 = Factor("P(B|A,H)", [b,a,h])
F3 = Factor("P(C|B,G)", [c,b,g])
F4 = Factor("P(D|C,F)", [d,c,f])
F5 = Factor("P(E|C)", [e,c])
F6 = Factor("P(F)", [f])
F7 = Factor("P(G)", [g])
F8 = Factor("P(H)", [h])
F9 = Factor("P(I|B)", [i,b])

F1.add_values([
    ['0', 0.1], 
    ['1', 0.9]])
F2.add_values([
    ['0', '0', '0', 0.4], 
    ['1', '0', '0', 0.6], 
    ['0', '0', '1', 0.5], 
    ['1', '0', '1', 0.5], 
    ['0', '1', '0', 1.0], 
    ['1', '1', '0', 0.0], 
    ['0', '1', '1', 0.0], 
    ['1', '1', '1', 1.0]])
F3.add_values([
    ['0', '0', '0', 0.0], 
    ['1', '0', '0', 1.0], 
    ['0', '0', '1', 0.9], 
    ['1', '0', '1', 0.1], 
    ['0', '1', '0', 0.1], 
    ['1', '1', '0', 0.9], 
    ['0', '1', '1', 0.1], 
    ['1', '1', '1', 0.9]])
F4.add_values([
    ['0', '0', '0', 0.8], 
    ['1', '0', '0', 0.2], 
    ['0', '0', '1', 0.3], 
    ['1', '0', '1', 0.7], 
    ['0', '1', '0', 0.0], 
    ['1', '1', '0', 1.0], 
    ['0', '1', '1', 1.0], 
    ['1', '1', '1', 0.0]])
F5.add_values([
    ['0','0',0.6],
    ['1','0',0.4],
    ['0','1',0.8],
    ['1','1',0.2]])
F6.add_values([
    ['0', 0.9],
    ['1',0.1]])
F7.add_values([
    ['0', 0.0],
    ['1',1.0]])
F8.add_values([
    ['0', 0.5],
    ['1', 0.5]])
F9.add_values([
    ['0', '0', 0.1],
    ['1', '0', 0.9],
    ['0', '1', 0.7],
    ['1', '1', 0.3]])

sn = BN('simple', [a,b,c,d,e,f,g,h,i], [F1,F2,F3,F4,F5,F6,F7,F8,F9])

if __name__ == '__main__':
    print("(a)")
    a.set_evidence('1')
    probs=VE(sn, b, [a])
    print("Pr(b|a) = {0:0.2f}".format(probs[1]))

    print("\n(b)")
    a.set_evidence('1')
    probs=VE(sn, c, [a])
    print("Pr(c|a) = {0:0.2f}".format(probs[1]))

    print("\n(c)")
    a.set_evidence('1')
    e.set_evidence('0')
    probs=VE(sn, c, [a,e])
    print("Pr(c|a,-e) = {0:0.2f}".format(probs[1]))

    print("\n(d)")
    a.set_evidence('1')
    f.set_evidence('0')
    probs=VE(sn, c, [a,f])
    print("Pr(c|a,-f) = {0:0.2f}".format(probs[1]))
