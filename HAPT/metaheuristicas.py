'''
@author: leo
'''
from problema import Solucao,gerarVizinhoTHPMD,gerarVizinhoTHPDD,gerarVizinhoTTEP,gerarVizinhoTPD
import random,copy

def buscaLocalBestImprovement(solucaoInicial,geradorDeVizinhanca):
    melhor = solucaoInicial
    for vizinho in geradorDeVizinhanca:
        if vizinho.beneficio() > melhor.beneficio():
            melhor = vizinho
    
    return melhor

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

def GRASP_VND(MAX_ITERACOES,instancia,alfa):
    melhorSolucao = Solucao(instancia)
    
    for k in range(MAX_ITERACOES):
        print(" GRASP: Iteracao %s"% (k+1))
        
        solucaoCorrente = construcao(instancia,alfa)
        
        # print("\n    Beneficio apos construcao:", solucaoCorrente.beneficio())
        
        solucaoCorrente = VNS_VND(5,instancia,solucaoCorrente)
        
#         print("\n    Beneficio apos VND:", solucaoCorrente.beneficio())
        
        if melhorSolucao.beneficio() < solucaoCorrente.beneficio():
            melhorSolucao = copy.deepcopy(solucaoCorrente)
            
    return melhorSolucao  

def construcao(instancia,alfa):
#     print("    Construindo solucao com alfa = %s"%str(alfa))
    
    solucao = Solucao(instancia)
    turmaDisciplinaToCargaDisponivelDic = solucao.instancia.turmaDisciplinaToCargaDic
    
    while not solucao.completa():
    
        geradorDeCandidatos = gerarCandidatos(solucao,turmaDisciplinaToCargaDisponivelDic)   
        todosCandidatos = [(slot,solucao.custoIncremental(slot)[1]) for slot in geradorDeCandidatos]   
        
        if todosCandidatos:
            todosCandidatos.sort(key=lambda x: x[1], reverse=True)
         
            RCL = [ c for c in todosCandidatos if custo(c) >= \
                   custo(todosCandidatos[0]) - alfa*(custo(todosCandidatos[0]) - custo(todosCandidatos[-1])) ]
                
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
            
def tupla(candidato):
    return candidato[0]

def custo(candidato):
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

def VNS_VND(MAX_ITERACOES_SEM_MELHORA,instancia,solucao):
    vizinhancas = [gerarVizinhoTHPMD,gerarVizinhoTHPDD,gerarVizinhoTTEP,gerarVizinhoTPD]
     
    # solucao = construcao(instancia, 1)
    # print("\n    Custo da solucao aleatoria inicial:",solucao.beneficio())
     
    i = 0
    while i < MAX_ITERACOES_SEM_MELHORA:
        # print("\nVNS: Iteracao %s"% i)

        solucaoAnterior = solucao
        
        k= 0
        while k < len(vizinhancas):
            
            geradorDeVizinhanca = vizinhancas[k](solucao)
            todosVizinhos = [vizinho for vizinho in geradorDeVizinhanca]           
             
            vizinhoAleatorio = random.choice(todosVizinhos)
            # print("\n    Custo do vizinho aleatorio na vizinhanca %s: %s" % (k, vizinhoAleatorio.beneficio()))
             
            vizinhoVND = VND(vizinhoAleatorio)
            # print("\n    Custo apos VND:", vizinhoVND.beneficio())
             
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
