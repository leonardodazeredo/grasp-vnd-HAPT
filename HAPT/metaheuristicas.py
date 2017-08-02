'''
@author: leo
'''
from problema import Solucao,gerarVizinhoTHPMD,gerarVizinhoTHPDD,gerarVizinhoTTEP,gerarVizinhoTPD
import random,copy
import logger

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

                candidato = (disciplina[0],professor)

                s = copy.deepcopy(solucao)
                s.setSlot(turmaNome,i,j,candidato)

                if s.restricaoA() and s.restricaoD():
                    turmaDisciplinaToCargaDisponivelDic[turmaNome,disciplina[0]]-= 1
                    yield candidato

def buscaLocalBestImprovement(solucaoInicial,geradorDeVizinhanca):
    melhor = solucaoInicial
    for vizinho in geradorDeVizinhanca:
        if vizinho.beneficio() > melhor.beneficio():
            melhor = vizinho

    return melhor

def construcao(instancia,alfa):
    logger.log("    Construindo solucao com alfa = %s" % str(alfa), logger.debugModeTotal)

    solucao = Solucao(instancia)
    turmaDisciplinaToCargaDisponivelDic = solucao.instancia.turmaDisciplinaToCargaDic

    while not solucao.completa():

        geradorDeCandidatos = gerarCandidatos(solucao, turmaDisciplinaToCargaDisponivelDic)
        todosCandidatos = [(candidato,solucao.beneficioIncremental(candidato)[1]) for candidato in geradorDeCandidatos]

        if todosCandidatos:
            todosCandidatos.sort(key=lambda x: x[1], reverse=True)

            RCL = [ c for c in todosCandidatos if getBeneficio(c) >= getBeneficio(todosCandidatos[0]) - alfa*(getBeneficio(todosCandidatos[0]) - getBeneficio(todosCandidatos[-1])) ]

            aleatorio = random.SystemRandom().choice(RCL)[0]

            (turmaNome,i,j) = solucao.slotVazio()
            turmaDisciplinaToCargaDisponivelDic[turmaNome,aleatorio[0]]-= 1
            solucao.adicionar(aleatorio)

        else:
            (turmaNome,i,j) = solucao.slotVazio()

            logger.log("    Reiniciando construcao: Nenhum candidato para o slot (%d,%d) da turma %s." % (i,j,turmaNome), logger.debugModeTotal)

            # random.shuffle(instancia.turmas)
            solucao = Solucao(instancia)
            turmaDisciplinaToCargaDisponivelDic = solucao.instancia.turmaDisciplinaToCargaDic

    return solucao



def GRASP_VND(MAX_ITERACOES,instancia,alfa):
    melhorSolucao = Solucao(instancia)

    for k in range(MAX_ITERACOES):
        logger.log(" GRASP: Iteracao %s" % (k+1), logger.debugModeTotal)

        solucaoCorrente = construcao(instancia,alfa)

        logger.log("\n    Beneficio apos construcao: %s" % solucaoCorrente.beneficio(), logger.debugModeTotal)

        solucaoCorrente = VND(solucaoCorrente)

        logger.log("\n    Beneficio apos VND: %s" % solucaoCorrente.beneficio(), logger.debugModeTotal)

        if melhorSolucao.beneficio() < solucaoCorrente.beneficio():
            melhorSolucao = copy.deepcopy(solucaoCorrente)

    return melhorSolucao

def GRASP_VNS_VND(MAX_ITERACOES,instancia,alfa):
    melhorSolucao = Solucao(instancia)

    for k in range(MAX_ITERACOES):
        logger.log(" GRASP: Iteracao %s" % k, logger.debugModeTotal)

        solucaoCorrente = construcao(instancia,alfa)

        logger.log("\n    Beneficio apos construcao: %s" % solucaoCorrente.beneficio(), logger.debugModeTotal)

        solucaoCorrente = VNS_VND(1,instancia,solucaoCorrente)

        logger.log("\n    Beneficio apos VND: %s" % solucaoCorrente.beneficio(), logger.debugModeTotal)

        if melhorSolucao.beneficio() < solucaoCorrente.beneficio():
            melhorSolucao = copy.deepcopy(solucaoCorrente)

    return melhorSolucao

def VNS_VND(MAX_ITERACOES_SEM_MELHORA,instancia,solucaoInicial=None):

    if solucaoInicial is not None:
        solucao = solucaoInicial
    else:
        random.shuffle(instancia.turmas)
        solucao = construcao(instancia, 1)

    logger.log("Iniciando VNS com VND")

    vizinhancas = [gerarVizinhoTHPMD,gerarVizinhoTHPDD,gerarVizinhoTTEP,gerarVizinhoTPD]

    logger.log("\n    Beneficio da solucao inicial: %s" % solucao.beneficio(), logger.debugModeTotal)

    i = 0
    while i < MAX_ITERACOES_SEM_MELHORA:
        # print("\nVNS: Iteracao %s"% i)

        solucaoAnterior = solucao

        k= 0
        while k < len(vizinhancas):

            geradorDeVizinhanca = vizinhancas[k](solucao)
            todosVizinhos = [vizinho for vizinho in geradorDeVizinhanca]

            vizinhoAleatorio = random.SystemRandom().choice(todosVizinhos)
            logger.log("\n    Beneficio do vizinho aleatorio na vizinhanca %s: %s" % (k, vizinhoAleatorio.beneficio()), logger.debugModeTotal)

            vizinhoVND = VND(vizinhoAleatorio)
            logger.log("\n    Beneficio apos VND: %s" % vizinhoVND.beneficio(), logger.debugModeTotal)

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
