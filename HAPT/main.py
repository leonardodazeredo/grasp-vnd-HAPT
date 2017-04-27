'''
@author: leo
'''

from problema import Solucao,beneficio
from metaheuristicas import GRASP_VND,VNS_VND,GRASP_VNS_VND,construcao
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


def VNS_VND_test():
    instancia = Instancia()

    for i in range(100):
        print("Teste %s VNS_VND " % (i))

        solucao = VNS_VND(10,instancia,construcao(instancia, 1))

        print("\nBeneficio da solucao:",beneficio(solucao))
        print("Solucao valida" if solucao.valida() else "Solucao invalida")

        print('\n------------------------------------------------------------------------------------\n')


def GRASP_VND_test():
    instancia = Instancia()

    melhorSolucao = (construcao(instancia, 1), -1, -1)

    for alfa in [.0, .25, .50, .75, 1.0]:
        print("Teste GRASP_VND com alfa = %s" % (alfa))

        solucao = GRASP_VND(100, instancia, alfa)

        if beneficio(solucao) > beneficio(melhorSolucao[0]):
            melhorSolucao = (solucao,alfa)

        print("\nBeneficio da solucao:",beneficio(solucao))
        print("Solucao valida" if solucao.valida() else "Solucao invalida")

        print('\n------------------------------------------------------------------------------------\n')

    melhorSolucao[0].printSolucao()
    print("Alfa: " + melhorSolucao[1])


def GRASP_VNS_VND_test():
    instancia = Instancia()

    melhorSolucao = (construcao(instancia, 1), -1, -1)

    for alfa in [.0, .25, .50, .75, 1.0]:
        print("Teste GRASP_VNS_VND com alfa = %s" % (alfa))

        solucao = GRASP_VNS_VND(100, instancia, alfa)

        if beneficio(solucao) > beneficio(melhorSolucao[0]):
            melhorSolucao = (solucao,alfa)

        print("\nBeneficio da solucao:",beneficio(solucao))
        print("Solucao valida" if solucao.valida() else "Solucao invalida")

        print('\n------------------------------------------------------------------------------------\n')

    melhorSolucao[0].printSolucao()
    print("Alfa: " + melhorSolucao[1])


if __name__ == '__main__':
    # VNS_VND_test()
    # GRASP_VND_test()
    GRASP_VNS_VND_test()

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
    #
    # solucao = VNS_VND(50,instancia,solucao)
    # solucao.printSolucao()
    #
    # solucao.printSolucao()
