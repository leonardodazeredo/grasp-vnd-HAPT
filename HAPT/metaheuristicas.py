'''
@author: leo
'''
from problema import Solucao,gerarVizinhoTHPMD,gerarVizinhoTHPDD,gerarVizinhoTTEP,gerarVizinhoTPD
import random,copy

def getAtividade(candidato):
    return candidato[0]

def getBeneficio(candidato):
    return candidato[1]

def gerarCandidatos(solucao,turmaDisciplinaToCargaDisponivelDic):
    (turmaNome,i,j) = solucao.slotVazio()

    turmaDisciplinaToCargaDisponivelDic = copy.deepcopy(turmaDisciplinaToCargaDisponivelDic)

    for disciplina in solucao.instancia.disciplinasDaTurma(turmaNome):
        if turmaDisciplinaToCargaDisponivelDic[turmaNome,disciplina[0]] > 0:

            for professor in solucao.instancia.professoresHabilitados(disciplina):

                slot = (disciplina[0],professor)

                s = copy.deepcopy(solucao)
                s.setSlot(turmaNome,i,j,slot)

                if s.restricaoA() and s.restricaoD():
                    turmaDisciplinaToCargaDisponivelDic[turmaNome,disciplina[0]]-= 1
                    yield slot

def buscaLocalBestImprovement(solucaoInicial,geradorDeVizinhanca):
    melhor = solucaoInicial
    for vizinho in geradorDeVizinhanca:
        if vizinho.beneficio() > melhor.beneficio():
            melhor = vizinho

    return melhor

def construcao(instancia,alfa):
#     print("    Construindo solucao com alfa = %s"%str(alfa))

    solucao = Solucao(instancia)
    turmaDisciplinaToCargaDisponivelDic = solucao.instancia.turmaDisciplinaToCargaDic

    while not solucao.completa():

        geradorDeCandidatos = gerarCandidatos(solucao,turmaDisciplinaToCargaDisponivelDic)
        todosCandidatos = [(slot,solucao.beneficioIncremental(slot)[1]) for slot in geradorDeCandidatos]

        if todosCandidatos:
            todosCandidatos.sort(key=lambda x: x[1], reverse=True)

            RCL = [ c for c in todosCandidatos if getBeneficio(c) >= getBeneficio(todosCandidatos[0]) - alfa*(getBeneficio(todosCandidatos[0]) - getBeneficio(todosCandidatos[-1])) ]

            aleatorio = random.choice(RCL)[0]

            (turmaNome,i,j) = solucao.slotVazio()
            turmaDisciplinaToCargaDisponivelDic[turmaNome,aleatorio[0]]-= 1
            solucao.adicionar(aleatorio)

        else:
            (turmaNome,i,j) = solucao.slotVazio()
#             print("    Reiniciando construcao: Nenhum candidato para o slot (%d,%d) da turma %s." % (i,j,turmaNome))

            solucao = Solucao(instancia)
            turmaDisciplinaToCargaDisponivelDic = solucao.instancia.turmaDisciplinaToCargaDic

    return solucao



def GRASP_VND(MAX_ITERACOES,instancia,alfa):
    melhorSolucao = Solucao(instancia)

    for k in range(MAX_ITERACOES):
        # print(" GRASP: Iteracao %s"% (k+1))

        solucaoCorrente = construcao(instancia,alfa)

        # print("\n    Beneficio apos construcao:", solucaoCorrente.beneficio())

        solucaoCorrente = VND(solucaoCorrente)

#         print("\n    Beneficio apos VND:", solucaoCorrente.beneficio())

        if melhorSolucao.beneficio() < solucaoCorrente.beneficio():
            melhorSolucao = copy.deepcopy(solucaoCorrente)

    return melhorSolucao

def GRASP_VNS_VND(MAX_ITERACOES,instancia,alfa):
    melhorSolucao = Solucao(instancia)

    for k in range(MAX_ITERACOES):
        # print(" GRASP: Iteracao %s"% (k+1))

        solucaoCorrente = construcao(instancia,alfa)

        # print("\n    Beneficio apos construcao:", solucaoCorrente.beneficio())

        solucaoCorrente = VNS_VND(1,instancia,solucaoCorrente)

        print(k)
#         print("\n    Beneficio apos VND:", solucaoCorrente.beneficio())

        if melhorSolucao.beneficio() < solucaoCorrente.beneficio():
            melhorSolucao = copy.deepcopy(solucaoCorrente)

    return melhorSolucao

def VNS_VND(MAX_ITERACOES_SEM_MELHORA,instancia,solucao):
    vizinhancas = [gerarVizinhoTHPMD,gerarVizinhoTHPDD,gerarVizinhoTTEP,gerarVizinhoTPD]

    # solucao = construcao(instancia, 1)
    # print("\n    Beneficio da solucao aleatoria inicial:",solucao.beneficio())

    i = 0
    while i < MAX_ITERACOES_SEM_MELHORA:
        # print("\nVNS: Iteracao %s"% i)

        solucaoAnterior = solucao

        k= 0
        while k < len(vizinhancas):

            geradorDeVizinhanca = vizinhancas[k](solucao)
            todosVizinhos = [vizinho for vizinho in geradorDeVizinhanca]

            vizinhoAleatorio = random.SystemRandom().choice(todosVizinhos)
            # print("\n    Beneficio do vizinho aleatorio na vizinhanca %s: %s" % (k, vizinhoAleatorio.beneficio()))

            vizinhoVND = VND(vizinhoAleatorio)
            # print("\n    Beneficio apos VND:", vizinhoVND.beneficio())

            if vizinhoVND.beneficio() > solucao.beneficio():
                solucao = vizinhoVND
                k = 0
            else:
                k+= 1

        if solucaoAnterior.beneficio() >= solucao.beneficio():
            i+= 1
        else:
            i = 0
            solucaoAnterior = solucao

        # print("\n"+str(i)+"\n")

    return solucao

def VND(solucaoInicial):
    vizinhancas = [gerarVizinhoTHPMD,gerarVizinhoTHPDD,gerarVizinhoTTEP,gerarVizinhoTPD]

    solucaoCorrente = copy.deepcopy(solucaoInicial)

    k= 0
    while k < len(vizinhancas):

        geradorDeVizinhanca = vizinhancas[k](solucaoCorrente)

        vizinhoCorrente = buscaLocalBestImprovement(solucaoCorrente,geradorDeVizinhanca)

        if vizinhoCorrente.beneficio() > solucaoCorrente.beneficio():
            solucaoCorrente = vizinhoCorrente
            k = 0
        else:
            k+= 1

    return solucaoCorrente
