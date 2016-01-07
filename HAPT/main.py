'''
@author: leo
'''

# from problema import Solucao
from metaheuristicas import GRASP_VND
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

def rodar(alfa,medias):
    #print("Iniciando Thread alfa =",alfa)
    beneficios = []
 
    for i in range(20):     

        print("GRASP iteracao %s Alfa = %s" % (i,alfa))
        solucao = GRASP_VND(30, instancia, alfa)  
        print("Terminou GRASP iteracao %s Alfa = %s" % (i,alfa))

        beneficios.append(solucao.beneficio())

    medias[alfa] = np.mean(beneficios)
    print("Beneficio: %s Alfa: %s" % (medias[alfa],alfa))

if __name__ == '__main__':
    instancia = Instancia()
    
    solucao = GRASP_VND(600,instancia,.25)     
    solucao.printSolucao()

    # medias = {}

    # threads = []
    # # for alfa in [.0, .25, .50, .75]:
    # for alfa in [.1, .2, .3]:
    #     threads.append(th.Thread(target=rodar, args=(alfa,medias,)))
    # for t in threads:
    #     t.start()
    # for t in threads:
    #     t.join()

    # print("--------------------------------------------------------")
    # for alfa in sorted(medias.keys()):
    #     print("Beneficio: %s Alfa: %s" % (medias[alfa],alfa))
        
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