'''
@author: leo
'''
import copy

class Solucao(object):
    '''
    Representa a solucao para o problema
    '''

    def __init__(self, instancia):
        '''
        Inicia uma solucao completamente vazia
        '''
        
        self.instancia = instancia
        
        self.alocacoes = {}
        
        for turma in instancia.turmas:
            alocacao = []
            for i in range(0,2):
                alocacao.append([None,None,None,None,None])
            
            self.alocacoes[turma] = alocacao
    
    def completa(self):
        gerador = self.gerarSlots()
        
        for slot in gerador:
            if slot[1] is None:
                return False
        
        return True
    
    def slotVazio(self):
        gerador = self.gerarSlots()
        
        for slot in gerador:
            #print(slot)
            if slot[1] is None:
                return slot[0],slot[2],slot[3]
        
        return None
    
    def adicionar(self,slot):
        for turmaNome in self.instancia.turmas:
            for j in range(0,5):
                for i in range(0,2):
                    if self.alocacoes[turmaNome][i][j] is None:
                        self.setSlot(turmaNome, i, j, slot)
                        return
    
    def gerarSlots(self):
        for turmaNome in self.instancia.turmas:
            for j in range(0,5):
                for i in range(0,2):
                    yield turmaNome,self.alocacoes[turmaNome][i][j],i,j
    
    def printSolucao(self):
        print('------------------------------------------------------------------------------------')
        for turmaNome in self.instancia.turmas:
            matrizAlocacoesTurma = self.alocacoes[turmaNome]
            print("\nTurma", turmaNome)
            for e in matrizAlocacoesTurma:
                print(e)
                
        print("\nBeneficio da solucao:",beneficio(self))
        print("Solucao valida" if self.valida() else "Solucao invalida")
        print('------------------------------------------------------------------------------------')
    
    def getSlot(self,tuplaTurmaTempoDia):
        return self.alocacoes[tuplaTurmaTempoDia[0]][tuplaTurmaTempoDia[1]][tuplaTurmaTempoDia[2]]
    
    def setSlot(self,turma,tempo,dia,alocacaoSlot):
        self.alocacoes[turma][tempo][dia] = alocacaoSlot
    
    def valida(self):
        
        restricoesDeInstancia = self.restricoesDeInstancia()
        restricaoA = self.restricaoA()  
        restricaoB = self.restricaoB()
        restricaoD = self.restricaoD()
        
#         if not restricoesDeInstancia:
#             print('Soucao viola as restricoes de instancia')
#         if not restricaoA:
#             print('Solucao viola a restricao A')
#         if not restricaoB:
#             print('Solucao viola a restricao B')
#         if not restricaoD:
#             print('Solucao viola a restricao D')
        
        return restricoesDeInstancia and restricaoA and restricaoB and restricaoD
        #restricaoC = True # trivialmente validada pela representacao da solucao
    
    def restricoesDeInstancia(self):
        slots = self.gerarSlots()
        
        for slot in slots:
            if slot[1] is not None:
                if slot[1][0] not in self.instancia.nomesDisciplinasDaTurma(slot[0])\
                or slot[1][1] not in self.instancia.professoresHabilitadosDisciplinaNome(slot[1][0]):
                    return False
        
        return True
    
    def restricaoA(self):
        '''
        Um professor nao pode dar mais de uma aula em slot de mesmo horario/dia em mais de 1 turma ao mesmo tempo.
        '''
        restricaoA = True
        duplicados = False
        
        lista = []
        for i in range(0,2):
            for j in range(0,5):
                if not duplicados:
                    lista = []
                    
                    for turmaNome in sorted(self.alocacoes.keys()):
                        matrizAlocacoesTurma = self.alocacoes[turmaNome]
                        if matrizAlocacoesTurma[i][j] is not None and not self.instancia.vaga(matrizAlocacoesTurma[i][j]):
                            lista.append(matrizAlocacoesTurma[i][j][1])
                     
                    countdic = {}
                    
                    for professori in lista:
                        if countdic.get(professori,None) is None:
                            countdic[professori] = True 
                        else:
                            duplicados = True
                            break
                
                if duplicados:

                    restricaoA = False
                    break
        
        if not restricaoA:
#             print("restricao A violada")
            return False
        
        return True
    
    def restricaoB(self):
        '''
        A disciplina deve cumprir sua carga
        '''
        restricaoB =True
        
        matrizAlocacoesTurma = []
        
        for turmaNome in sorted(self.alocacoes.keys()):
            if restricaoB:
                
                matrizAlocacoesTurma = self.alocacoes[turmaNome]

                disciplinaCargaDic = {}
                
                for i in range(0,2):
                    for j in range(0,5):
                        if matrizAlocacoesTurma[i][j] is not None:
                            
                            if disciplinaCargaDic.get(matrizAlocacoesTurma[i][j][0], None) is not None:
                                disciplinaCargaDic[matrizAlocacoesTurma[i][j][0]]+= 1 
                            else:
                                disciplinaCargaDic[matrizAlocacoesTurma[i][j][0]] = 1
                
                disciplinasDaTurma = self.instancia.disciplinasDaTurma(turmaNome)
                
                for disciplina in sorted(disciplinaCargaDic.keys()):
                    
                    if not self.instancia.vagaNome(disciplina):
                        cargaDaDisciplina = [c for (n,c) in disciplinasDaTurma if n == disciplina][0]
    
                        if int(cargaDaDisciplina) != int(disciplinaCargaDic[disciplina]):
                            restricaoB = False
                            break
                
        if not restricaoB:
#             print("restricao B violada")
            return False
        
        return True
        
    def restricaoD(self):
        '''
        Cada disciplina só pode ter 1 professor, dentro de uma mesma turma
        '''
        restricaoD = True
         
        for turmaNome in sorted(self.alocacoes.keys()):
            if restricaoD:
             
                matrizAlocacoesTurma = self.alocacoes[turmaNome]
                disciplinaCargaDic = {}
                 
                for i in range(0,2):
                    for j in range(0,5):
                        if matrizAlocacoesTurma[i][j] is not None:
                            if disciplinaCargaDic.get(matrizAlocacoesTurma[i][j][0], None) is None:
                                disciplinaCargaDic[matrizAlocacoesTurma[i][j][0]] = matrizAlocacoesTurma[i][j][1] 
                                 
                            elif disciplinaCargaDic[matrizAlocacoesTurma[i][j][0]] != matrizAlocacoesTurma[i][j][1]:
                                restricaoD = False
                                break
                 
        if not restricaoD:
#             print("restricao D violada")
            return False
        
        return True
    
    def beneficio(self):
        return beneficio(self)
    
    def custoIncremental(self,slot):
        solucaoIncrementada = copy.deepcopy(self)
        
        solucaoIncrementada.adicionar(slot)
        
        return solucaoIncrementada,beneficio(solucaoIncrementada)
        
def beneficio(solucao):
    beneficio = 0
#     z = 0
    for turmaNome in solucao.alocacoes.keys():
        matrizAlocacoesTurma = solucao.alocacoes[turmaNome]
        
        for i in range(0,2):
            for j in range(0,5):
                if matrizAlocacoesTurma[i][j] is not None and not solucao.instancia.vaga(matrizAlocacoesTurma[i][j]):
                    beneficio+= solucao.instancia.getPreferencia(matrizAlocacoesTurma[i][j][1],i,j)
        
        for j in range(0,5):
            if matrizAlocacoesTurma[0][j] is not None and matrizAlocacoesTurma[1][j] is not None:
                if matrizAlocacoesTurma[0][j][0] == matrizAlocacoesTurma[1][j][0]:
#                     z+=1
#                     print(z,'iguais')
                    beneficio+= 5
                
    return beneficio


def carregaTeste(solucao):
    testePath = 'dataset/testeSolucao'
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
        