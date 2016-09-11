##Three sample bayes nets are defined here. 
##
from bnet import *

VisitAsia = Variable('Visit_To_Asia', ['visit', 'no-visit'])
F1 = Factor("F1", [VisitAsia])
F1.add_values([['visit', 0.01], ['no-visit', 0.99]])

Smoking = Variable('Smoking', ['smoker', 'non-smoker'])
F2 = Factor("F2", [Smoking])
F2.add_values([['smoker', 0.5], ['non-smoker', 0.5]])

Tuberculosis = Variable('Tuberculosis', ['present', 'absent'])
F3 = Factor("F3", [Tuberculosis, VisitAsia])
F3.add_values([['present', 'visit', 0.05],
               ['present', 'no-visit', 0.01],
               ['absent', 'visit', 0.95],
               ['absent', 'no-visit', 0.99]])

Cancer = Variable('Lung Cancer', ['present', 'absent'])
F4 = Factor("F4", [Cancer, Smoking])
F4.add_values([['present', 'smoker', 0.10],
               ['present', 'non-smoker', 0.01],
               ['absent', 'smoker', 0.90],
               ['absent', 'non-smoker', 0.99]])

Bronchitis = Variable('Bronchitis', ['present', 'absent'])
F5 = Factor("F5", [Bronchitis, Smoking])
F5.add_values([['present', 'smoker', 0.60],
               ['present', 'non-smoker', 0.30],
               ['absent', 'smoker', 0.40],
               ['absent', 'non-smoker', 0.70]])

TBorCA = Variable('Tuberculosis or Lung Cancer', ['true', 'false'])
F6 = Factor("F6", [TBorCA, Tuberculosis, Cancer])
F6.add_values([['true', 'present', 'present', 1.0],
               ['true', 'present', 'absent', 1.0],
               ['true', 'absent', 'present', 1.0],
               ['true', 'absent', 'absent', 0],
               ['false', 'present', 'present', 0],
               ['false', 'present', 'absent', 0],
               ['false', 'absent', 'present', 0],
               ['false', 'absent', 'absent', 1]])


Dyspnea = Variable('Dyspnea', ['present', 'absent'])
F7 = Factor("F7", [Dyspnea, TBorCA, Bronchitis])
F7.add_values([['present', 'true', 'present', 0.9],
               ['present', 'true', 'absent', 0.7],
               ['present', 'false', 'present', 0.8],
               ['present', 'false', 'absent', 0.1],
               ['absent', 'true', 'present', 0.1],
               ['absent', 'true', 'absent', 0.3],
               ['absent', 'false', 'present', 0.2],
               ['absent', 'false', 'absent', 0.9]])


Xray = Variable('XRay Result', ['abnormal', 'normal'])
F8 = Factor("F8", [Xray, TBorCA])
F8.add_values([['abnormal', 'true', 0.98],
               ['abnormal', 'false', 0.05],
               ['normal', 'true', 0.02],
               ['normal', 'false', 0.95]])

Asia = BN("Asia", [VisitAsia, Smoking, Tuberculosis, Cancer,
                   Bronchitis, TBorCA, Dyspnea, Xray],
                   [F1, F2, F3, F4, F5, F6, F7, F8])

## E,B,S,w,G example from sample questions
F = Variable('F', ['f', '-f'])
B = Variable('B', ['b', '-b'])
S = Variable('S', ['s', '-s'])
C = Variable('C', ['c', '-c'])
M = Variable('M', ['m', '-m'])
FS = Factor('P(S)', [S])
FB = Factor('P(B|S)', [B,S])
FF = Factor('P(F|B,C)', [F, B, C])
FC = Factor('P(C|S)', [C,S])
FM = Factor('P(M|C)', [M,C])

FS.add_values([['s',0.2], ['-s', 0.8]])
FB.add_values([['-b','-s', 0.95], ['b','-s', 0.05],['-b','s',0.75],['b','s',0.25]])
FF.add_values([['-f', '-b', '-c', .95], ['f', '-b', '-c', .05], ['-f', '-b', 'c', .5],['f', '-b', 'c', 0.5],
               ['-f', 'b', '-c', .9], ['f', 'b', '-c', .1], ['-f', 'b', 'c', .25],['f', 'b', 'c', 0.75]])
FC.add_values([['-c', '-s', 0.99], ['c', '-s', 0.01], ['-c', 's', 0.98], ['c', 's', 0.02]])
FM.add_values([['m', 'c', 0.6], ['m', '-c', .02], ['-m', 'c', 0.4], ['-m', '-c', 0.98]])

Q3 = BN('SampleQ4', [F,B,S,C,M], [FF,FB,FS,FC,FM])

if __name__ == '__main__':
    #(a)
    print("Question (a)")
    F.set_evidence('f')
    probs = VE(Q3, S, [F])
    print('P(s|f) = {} P(-s|f) = {}'.format(probs[0], probs[1]))

    #(b)
    print("\nQuestion (b)")
    B.set_evidence('b')
    E.set_evidence('-e')
    probs = VE(Q3, W, [B, E])
    print('P(w|b,-e) = {} P(-w|b,-e) = {}'.format(probs[0],probs[1]))

    #(c)
    print("\nQuestion (c)")
    S.set_evidence('s')
    probs1 = VE(Q3, G, [S])
    S.set_evidence('-s')
    probs2 = VE(Q3, G, [S])
    print('P(g|s) = {} P(-g|s) = {} P(g|-s) = {} P(-g|-s) = {}'.format(probs1[0],probs1[1],probs2[0],probs2[1]))

    #(d)
    print("\nQuestion (d)")
    S.set_evidence('s')
    W.set_evidence('w')
    probs1 = VE(Q3, G, [S,W])
    S.set_evidence('s')
    W.set_evidence('-w')
    probs2 = VE(Q3, G, [S,W])
    S.set_evidence('-s')
    W.set_evidence('w')
    probs3 = VE(Q3, G, [S,W])
    S.set_evidence('-s')
    W.set_evidence('-w')
    probs4 = VE(Q3, G, [S,W])
    print('P(g|s,w) = {} P(-g|s,w) = {} P(g|s,-w) = {} P(-g|s,-w) = {}'.format(probs1[0],probs1[1],probs2[0],probs2[1]))
    print('P(g|-s,w) = {} P(-g|-s,w) = {} P(g|-s,-w) = {} P(-g|-s,-w) = {}'.format(probs3[0],probs3[1],probs4[0],probs4[1]))

    #(e)
    print("\nQuestion (e)")
    print('Since P(G|S,W) = P(G|S) (i.e., this equation holds for every value of G, S, and W)')
    print('we have that G is conditionally independent of W given S.')
    
    #(f) 
    print("\nQuestion (f)")
    W.set_evidence('w')
    probs1 = VE(Q3, G, [W])
    W.set_evidence('-w')
    probs2 = VE(Q3, G, [W])
    print('P(g|w) = {} P(-g|w) = {} P(g|-w) = {} P(-g|-w) = {}'.format(probs1[0],probs1[1],probs2[0],probs2[1]))

    #(g) 
    print("\nQuestion (g)")
    print('Since the probability of G changes as we change the value of W, G is not independent of W')
    print('However d and e show that given S G becomes independent of W')


    #(h)
    print("\nExtra Note")
    print("VE can compute the unconditional probability of a variable by selecting no evidence variables")
    probs = VE(Q3, G, [])
    print('P(g) = {} P(-g) = {}'.format(probs[0], probs[1]))
    probs = VE(Q3, E, [])
    print('P(e) = {} P(-e) = {}'.format(probs[0], probs[1]))
    print("\nNow you can experiment with the Asia network")

