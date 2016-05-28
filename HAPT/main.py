'''
@author: leo
'''

# from problema import Solucao
from metaheuristicas import GRASP_VND,VNS_VND,construcao
from manipulaInstancia import Instancia
import numpy as np
import threading as th

def carregaTeste(solucao,testePath = 'dataset/testeSolucao'):
    slotsMatrix = []
    with open(testePath, encoding='utf-8', newline='\n') as testeSolucao:
        for linha in testeSolucao:  
            slots = linha.strip().split()
            if len(slots) > 0:
                slots = [('VAGA',None) if s.strip()=='VAGA' else (s.strip().split(',')[0],int(s.strip().split(',')[1])-1) for s in slots]
                slotsMatrix.append(slots)              
    for e,turmaNome in enumerate(sorted(solucao.instancia.turmas)): 
        for i in range(0,2):               
            for j in range(0,5):           
                    index = (e+1)*2 - (1+i)     
                    index = index - 1 if i == 0 else index + 1    
                    solucao.setSlot(turmaNome, i, j, slotsMatrix[index][j])
                    
def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

def rodarTesteAlfa(alfa):
    #print("Iniciando Thread alfa =",alfa)
    beneficios = []
 
    for i in range(4):     

        print("Teste %s GRASP_VND com alfa = %s" % (i+1,alfa))
        solucao = GRASP_VND(25, instancia, alfa)  
        print("Terminou teste %s GRASP_VND alfa = %s" % (i+1,alfa))

        beneficios.append(solucao.beneficio())

    print("Beneficio: %s Alfa: %s" % (np.mean(beneficios),alfa))

if __name__ == '__main__':
    instancia = Instancia()
    
    solucao = GRASP_VND(10,instancia,.25)     
    solucao.printSolucao()

    # solucao = VNS_VND(10,instancia,construcao(instancia, .25))     
    # solucao.printSolucao()

    # threads = []
    # # for alfa in [.0, .25, .50, .75]:
    # for alfa in [.1, .2, .3]:
    # # for alfa in [.3]:
    #     threads.append(th.Thread(target=rodarTesteAlfa, args=(alfa,)))
    # for t in threads:
    #     t.start()

    # for t in threads:
    #     t.join()

    # for d in instancia.disciplinas:
    #     print(d)   
    # print("\n")
    
    # for t in instancia.turmas:
    #     print(t,str(instancia.disciplinasDaTurma(t))) 
    # print("\n")
    
    # for i,t in enumerate(instancia.disciplinasDoProfessori):
    #     print(i,t)
    # print("\n")
        
    # for d in instancia.disciplinas:
    #     print(d,instancia.professoresHabilitados(d))
    # print("\n")

    # solucao = Solucao(instancia) 
    # carregaTeste(solucao)
    # solucao.printSolucao()