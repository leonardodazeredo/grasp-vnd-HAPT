'''
@author: leo
'''
from problema import *

import random

def trocaSlot(solucao,slot1,slot2):
    solucao = copy.deepcopy(solucao)
    
    novoSlot1 = copy.deepcopy(solucao.getSlot(slot1))
    novoSlot2 = copy.deepcopy(solucao.getSlot(slot2))
    
    solucao.setSlot(slot2[0],slot2[1],slot2[2],novoSlot1)
    
    solucao.setSlot(slot1[0],slot1[1],slot1[2],novoSlot2)  
    
    return solucao

def trocaTurma(solucao,slot1,slot2):
    solucao = copy.deepcopy(solucao)
    
    alocacao1 = copy.deepcopy(solucao.getSlot(slot1))
    alocacao2 = copy.deepcopy(solucao.getSlot(slot2))
    
    novaAlocacao = (alocacao2[0],alocacao1[1])
    solucao.setSlot(slot1[0],slot1[1],slot1[2],novaAlocacao)
    
    novaAlocacao = (alocacao1[0],alocacao2[1])
    solucao.setSlot(slot2[0],slot2[1],slot2[2],novaAlocacao)
    
    return solucao

def trocaProfessor(solucao,slot1,slot2):
    solucao = copy.deepcopy(solucao)
    
    alocacao1 = solucao.getSlot(slot1)
    alocacao2 = solucao.getSlot(slot2)
    
    novaAlocacao = (alocacao1[0],alocacao2[1])
    solucao.setSlot(slot1[0],slot1[1],slot1[2],novaAlocacao)
    
    novaAlocacao = (alocacao2[0],alocacao1[1])
    solucao.setSlot(slot2[0],slot2[1],slot2[2],novaAlocacao)
    
    return solucao

def trocaProfessorEntreTurmas(solucao,turma1,turma2,disciplina1,disciplina2):
    solucao = copy.deepcopy(solucao)
    
    professor1 = professor2 = None
    
    for j1 in range(0,5):
        for i1 in range(0,2):
            slot1 = solucao.getSlot((turma1,i1,j1))
            if slot1 is not None:
                if slot1[0] == disciplina1:
                    
                    if professor1 is None: professor1 = slot1[1]
                    
                    for j2 in range(0,5):
                        for i2 in range(0,2):
                            slot2 = solucao.getSlot((turma2,i2,j2))
                            if slot2 is not None:
                                if slot2[0] == disciplina2:
                                    
                                    if professor2 is None: professor2 = slot2[1]
                                    
                                    novoSlot = (slot1[0],professor2)
                                    solucao.setSlot(turma1,i1,j1,novoSlot)
                                    
                                    novoSlot = (slot2[0],professor1)
                                    solucao.setSlot(turma2,i2,j2,novoSlot)
    
    return solucao

def trocaProfessorDaDisciplinaNaTurma(solucao,turmaNome,disciplina,professor):
    solucao = copy.deepcopy(solucao)
               
    for j in range(0,5):
        for i in range(0,2):
            slot = solucao.getSlot((turmaNome,i,j))       
            if slot is not None:   
                if slot[0] == disciplina:
                    slot = (slot[0],professor)
                    solucao.setSlot(turmaNome,i,j,slot)

    return solucao
    

def gerarVizinhoTHPMD(solucao):
    
    slots = {}
    
    for j in range(0,5):
        for turmaNome in solucao.instancia.turmas:
            matrizAlocacoesTurma = solucao.alocacoes[turmaNome] 
            
            for i in range(0,2):
                slots[(turmaNome,i,j)] = matrizAlocacoesTurma[i][j]
    
        chaves   = sorted(list(slots.keys()))
        
        for i in range(0, len(list(slots.keys()))-1):
            for j in range(i+1,len(list(slots.keys()))):              
                s = None         
                #testando aqui a validade do movimento segundo as restricoes de instancia
                if slots[chaves[i]] is not None and slots[chaves[j]] is not None:
                    
                    if slots[chaves[i]][1] != slots[chaves[j]][1]:
                        if slots[chaves[i]][0] in solucao.instancia.nomesDisciplinasDaTurma(chaves[j][0])\
                            and slots[chaves[j]][0] in solucao.instancia.nomesDisciplinasDaTurma(chaves[i][0]):
                            
                            s =  trocaSlot(solucao,chaves[i],chaves[j])
                    
                    elif not solucao.instancia.vaga(slots[chaves[i]]) and solucao.instancia.vaga(slots[chaves[j]]):
                        if slots[chaves[i]][0] in solucao.instancia.nomesDisciplinasDaTurma(chaves[j][0]):
                            
                            s =  trocaSlot(solucao,chaves[i],chaves[j])
                        
                    elif solucao.instancia.vaga(slots[chaves[i]]) and not solucao.instancia.vaga(slots[chaves[j]]):
                        if slots[chaves[j]][0] in solucao.instancia.nomesDisciplinasDaTurma(chaves[i][0]):
                            
                            s =  trocaSlot(solucao,chaves[i],chaves[j])
                    
                    if s is not None and s.valida():
#                         print('1')
                        yield s
                        
def gerarVizinhoTHPDD(solucao):
    for j1 in range(0,4):
        for turmaNome1 in solucao.instancia.turmas:
            for i1 in range(0,2):
                pivo1 = solucao.getSlot((turmaNome1,i1,j1))
                
                for j2 in range(j1+1,5):
                    for turmaNome2 in solucao.instancia.turmas:
                        for i2 in range(0,2):
                            pivo2 = solucao.getSlot((turmaNome2,i2,j2))                      

                            s = None        
                            
                            #testando aqui a validade do movimento segundo as restricoes de instancia
                            if pivo1 is not None and pivo2 is not None:
                                if pivo1[1] != pivo1[1]:
                                    if pivo1[0] in solucao.instancia.nomesDisciplinasDaTurma(turmaNome2)\
                                        and pivo2[0] in solucao.instancia.nomesDisciplinasDaTurma(turmaNome1):
                                        
                                        s =  trocaSlot(solucao,(turmaNome1,i1,j1),(turmaNome2,i2,j2))
                                
                                elif not solucao.instancia.vaga(pivo1) and solucao.instancia.vaga(pivo2):
                                    if pivo1[0] in solucao.instancia.nomesDisciplinasDaTurma(turmaNome2):
                                        
                                        s =  trocaSlot(solucao,(turmaNome1,i1,j1),(turmaNome2,i2,j2))
                                    
                                elif solucao.instancia.vaga(pivo1) and not solucao.instancia.vaga(pivo2):
                                    if pivo2[0] in solucao.instancia.nomesDisciplinasDaTurma(turmaNome1):
                                        
                                        s =  trocaSlot(solucao,(turmaNome1,i1,j1),(turmaNome2,i2,j2))
                                              
                                if s is not None and s.valida():
#                                     print('2')
                                    yield s

def gerarVizinhoTTEP(solucao):   
    for i,turmaNome1 in enumerate(solucao.instancia.turmas[0:-1]):
        for turmaNome2 in solucao.instancia.turmas[i+1:]:
            
            for i,disciplina1 in enumerate(solucao.instancia.disciplinasDaTurma(turmaNome1)[0:-1]):
                for disciplina2 in solucao.instancia.disciplinasDaTurma(turmaNome2)[i+1:]:

                    if not solucao.instancia.vaga(disciplina1) and not solucao.instancia.vaga(disciplina2):
                        s = trocaProfessorEntreTurmas(solucao,turmaNome1,turmaNome2,disciplina1[0],disciplina2[0])                   
                        if s is not None and s.valida():
#                             print('3')
                            yield s

def gerarVizinhoTPD(solucao):
    for turmaNome in solucao.instancia.turmas:
        for disciplina in solucao.instancia.disciplinasDaTurma(turmaNome):    
            if not solucao.instancia.vaga(disciplina): 
                for professoresHabilitado in solucao.instancia.professoresHabilitados(disciplina):               
                                   
                    s =  trocaProfessorDaDisciplinaNaTurma(solucao, turmaNome, disciplina[0], professoresHabilitado)                 
                    if s is not None and s.valida():
    #                    print('4')
                        yield s

def buscaLocalBestImprovement(solucaoInicial,geradorDeVizinhanca):
    melhor = solucaoInicial
    for vizinho in geradorDeVizinhanca:
        if beneficio(vizinho) > beneficio(melhor):
            melhor = vizinho
    
    return melhor

def VND(solucaoInicial):
    vizinhancas = [gerarVizinhoTHPMD,gerarVizinhoTHPDD,gerarVizinhoTTEP,gerarVizinhoTPD]
    
    solucaoCorrente = copy.deepcopy(solucaoInicial)
    
    k= 0
    while k < len(vizinhancas):
        
        geradorDeVizinhanca = vizinhancas[k](solucaoCorrente)
        
        vizinhoCorrente = buscaLocalBestImprovement(solucaoCorrente,geradorDeVizinhanca)
        
        if beneficio(vizinhoCorrente) > beneficio(solucaoCorrente):
            solucaoCorrente = vizinhoCorrente
            k = 0
        else:
            k+= 1
    
    return solucaoCorrente

def GRASP_VND(MAX_ITERACOES,instancia,alfa):
    melhorSolucao = Solucao(instancia)
    
    for k in range(MAX_ITERACOES):
        print("\nGRASP: Iteracao %s"% k)
        
        solucaoCorrente = construcao(instancia,alfa)
        
        print("\n    Custo apos construcao:", solucaoCorrente.beneficio())
        
        solucaoCorrente = VND(solucaoCorrente)
        
        print("    Custo apos VND:", solucaoCorrente.beneficio())
        
        beneficio = solucaoCorrente.beneficio()
        
        if melhorSolucao.beneficio() < beneficio:
            melhorSolucao = copy.deepcopy(solucaoCorrente)
            
    return melhorSolucao  

def construcao(instancia,alfa):
    print("    Construindo solucao com alfa = %s"%str(alfa))
    
    solucao = Solucao(instancia)
    turmaDisciplinaToCargaDisponivelDic = solucao.instancia.turmaDisciplinaToCargaDic
    
    while not solucao.completa():
    
        geradorDeCandidatos = gerarCandidatos(solucao,turmaDisciplinaToCargaDisponivelDic)   
        todosCandidatos = [(slot,solucao.custoIncremental(slot)[1]) for slot in geradorDeCandidatos]   
        
        if todosCandidatos:
            todosCandidatos.sort(key=lambda x: x[1], reverse=True)
         
#             print(todosCandidatos)
         
            RCL = [c for c in todosCandidatos if custo(c) >=  custo(todosCandidatos[0]) - alfa * (custo(todosCandidatos[0]) - custo(todosCandidatos[-1]))]
                
            aleatorio = random.choice(RCL)[0]
            
#             print(aleatorio)
    
            (turmaNome,i,j) = solucao.slotVazio()
            turmaDisciplinaToCargaDisponivelDic[turmaNome,aleatorio[0]]-= 1   
            solucao.adicionar(aleatorio)
            
        else:
            (turmaNome,i,j) = solucao.slotVazio()
            print("    Construcao: Nenhum candidato disponivel no slot (%d,%d) da turma %s. Reiniciando construcao." % (i,j,turmaNome))
#             solucao.printSolucao()
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
                    turmaDisciplinaToCargaDisponivelDic[turmaNome,disciplina[0]] -= 1     
                    yield slot

# def VNS_VND(MAX_ITERACOES,instancia):
#     vizinhancas = [gerarVizinhoTHPMD,gerarVizinhoTHPDD,gerarVizinhoTTEP,gerarVizinhoTPD]
#     
#     solucao = construcao(instancia, 1)
#     
# #     solucaoCorrente = copy.deepcopy(solucao)
#     
#     i = 0
#     while i < MAX_ITERACOES:
#         k= 0
#         print("iteracao",i)
#         while k < len(vizinhancas):
#             print("custo da solucao:",solucao.beneficio())
#             
#             geradorDeVizinhanca = vizinhancas[k](solucao)
#             todosVizinhos = [vizinho for vizinho in geradorDeVizinhanca]           
#             
#             vizinhoAleatorio = random.choice(todosVizinhos)
#             print("custo do vizinho aleatorio em :",k, vizinhoAleatorio.beneficio())
#             
#             vizinhoVND = VND(vizinhoAleatorio)
#             print("custo do vizinho apos VND:", vizinhoVND.beneficio())
#             
#             if beneficio(vizinhoVND) > beneficio(solucao):
#                 solucao = vizinhoVND
#                 k = 0
#             else:
#                 k+= 1
#                 
#             print("\n")
#         i+=1
#                 
#     return solucao