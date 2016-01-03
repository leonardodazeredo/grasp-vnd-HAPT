'''
@author: leo
'''

# from problema import Solucao
from metaheuristicas import GRASP_VND
from manipulaInstancia import Instancia
import numpy as np

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

if __name__ == '__main__':
    instancia = Instancia()
    
#     solucao = GRASP_VND(1,instancia,0.7)     
#     solucao.printSolucao()

    medias = {}
    
    for alfa in [0.00, 0.25, 0.50, 0.75, 1.00]:
        beneficios = []
        
        print("\nAlfa:",alfa)
        
        for i in range(10):    
            print("------",i)   
            solucao = GRASP_VND(10, instancia, alfa)  
            beneficios.append(solucao.beneficio())

        medias[alfa] = np.mean(beneficios)
        print("Media:",medias[alfa])
        
    
    for alfa in sorted(medias.keys()):
        print("Beneficio: %s Alfa: %s" % (medias[alfa],alfa))
        
 
#     for d in instancia.disciplinas:
#         print(d)   
#     print("\n")
#     
#     for t in instancia.turmas:
#         print(t,str(instancia.disciplinasDaTurma(t))) 
#     print("\n")
#     
#     for i,t in enumerate(instancia.disciplinasDoProfessori):
#         print(i,t)
#     print("\n")
#         
#     for d in instancia.disciplinas:
#         print(d,instancia.professoresHabilitados(d))
#     print("\n")
#
#     solucao = Solucao(instancia) 
#     carregaTeste(solucao)
#     solucao.printSolucao()