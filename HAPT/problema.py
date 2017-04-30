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

        self.valorBeneficio = None

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
        self.valorBeneficio = None
        self.alocacoes[turma][tempo][dia] = alocacaoSlot

    def valida(self):
        restricoesDeInstancia = self.restricoesDeInstancia()
        restricaoA = self.restricaoA()
        restricaoB = self.restricaoB()
        restricaoD = self.restricaoD()

        # if not restricoesDeInstancia:
        #     print('Soucao viola as restricoes de instancia')
        # if not restricaoA:
        #     print('Solucao viola a restricao A')
        # if not restricaoB:
        #     print('Solucao viola a restricao B')
        # if not restricaoD:
        #     print('Solucao viola a restricao D')

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
            # print("restricao A violada")
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

    # Metodos de troca
    def trocaSlot(self,slot1,slot2):
        solucao = copy.deepcopy(self)

        novoSlot1 = copy.deepcopy(solucao.getSlot(slot1))
        novoSlot2 = copy.deepcopy(solucao.getSlot(slot2))

        solucao.setSlot(slot2[0],slot2[1],slot2[2],novoSlot1)

        solucao.setSlot(slot1[0],slot1[1],slot1[2],novoSlot2)

        return solucao

    def trocaTurma(self,slot1,slot2):
        solucao = copy.deepcopy(self)

        alocacao1 = copy.deepcopy(solucao.getSlot(slot1))
        alocacao2 = copy.deepcopy(solucao.getSlot(slot2))

        novaAlocacao = (alocacao2[0],alocacao1[1])
        solucao.setSlot(slot1[0],slot1[1],slot1[2],novaAlocacao)

        novaAlocacao = (alocacao1[0],alocacao2[1])
        solucao.setSlot(slot2[0],slot2[1],slot2[2],novaAlocacao)

        return solucao

    def trocaProfessor(self,slot1,slot2):
        solucao = copy.deepcopy(self)

        alocacao1 = solucao.getSlot(slot1)
        alocacao2 = solucao.getSlot(slot2)

        novaAlocacao = (alocacao1[0],alocacao2[1])
        solucao.setSlot(slot1[0],slot1[1],slot1[2],novaAlocacao)

        novaAlocacao = (alocacao2[0],alocacao1[1])
        solucao.setSlot(slot2[0],slot2[1],slot2[2],novaAlocacao)

        return solucao

    def trocaProfessorEntreTurmas(self,turma1,turma2,disciplina1,disciplina2):
        solucao = copy.deepcopy(self)

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

    def trocaProfessorDaDisciplinaNaTurma(self,turmaNome,disciplina,professor):
        solucao = copy.deepcopy(self)
        for j in range(0,5):
            for i in range(0,2):
                slot = solucao.getSlot((turmaNome,i,j))
                if slot is not None:
                    if slot[0] == disciplina:
                        slot = (slot[0],professor)
                        solucao.setSlot(turmaNome,i,j,slot)

        return solucao

    def beneficio(self):
        if self.valorBeneficio is None:
            self.valorBeneficio = beneficio(self)
        return self.valorBeneficio

    def beneficioIncremental(self,slot):
        solucaoIncrementada = copy.deepcopy(self)
        solucaoIncrementada.adicionar(slot)

        return solucaoIncrementada,beneficio(solucaoIncrementada)

def beneficio(solucao):
    beneficio = 0
    for turmaNome in solucao.alocacoes.keys():
        matrizAlocacoesTurma = solucao.alocacoes[turmaNome]

        for i in range(0,2):
            for j in range(0,5):
                if matrizAlocacoesTurma[i][j] is not None and not solucao.instancia.vaga(matrizAlocacoesTurma[i][j]):
                    beneficio+= solucao.instancia.getPreferencia(matrizAlocacoesTurma[i][j][1],i,j)

        for j in range(0,5):
            if matrizAlocacoesTurma[0][j] is not None and matrizAlocacoesTurma[1][j] is not None:
                if matrizAlocacoesTurma[0][j][0] == matrizAlocacoesTurma[1][j][0]:
                    beneficio+= 5

    return beneficio

# Geradores de vizinhos para as 4 estruturas de vizinhancas
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

                # testando aqui a validade do movimento segundo as restricoes de instancia
                if slots[chaves[i]] is not None and slots[chaves[j]] is not None:

                    if slots[chaves[i]][1] != slots[chaves[j]][1]:
                        if slots[chaves[i]][0] in solucao.instancia.nomesDisciplinasDaTurma(chaves[j][0])\
                            and slots[chaves[j]][0] in solucao.instancia.nomesDisciplinasDaTurma(chaves[i][0]):

                            s =  solucao.trocaSlot(chaves[i],chaves[j])

                    elif not solucao.instancia.vaga(slots[chaves[i]]) and solucao.instancia.vaga(slots[chaves[j]]):
                        if slots[chaves[i]][0] in solucao.instancia.nomesDisciplinasDaTurma(chaves[j][0]):

                            s =  solucao.trocaSlot(chaves[i],chaves[j])

                    elif solucao.instancia.vaga(slots[chaves[i]]) and not solucao.instancia.vaga(slots[chaves[j]]):
                        if slots[chaves[j]][0] in solucao.instancia.nomesDisciplinasDaTurma(chaves[i][0]):

                            s =  solucao.trocaSlot(chaves[i],chaves[j])

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

                            # Testando a validade do movimento segundo as restricoes de instancia
                            if pivo1 is not None and pivo2 is not None:
                                if pivo1[1] != pivo1[1]:
                                    if pivo1[0] in solucao.instancia.nomesDisciplinasDaTurma(turmaNome2)\
                                        and pivo2[0] in solucao.instancia.nomesDisciplinasDaTurma(turmaNome1):

                                        s =  solucao.trocaSlot((turmaNome1,i1,j1),(turmaNome2,i2,j2))

                                elif not solucao.instancia.vaga(pivo1) and solucao.instancia.vaga(pivo2):
                                    if pivo1[0] in solucao.instancia.nomesDisciplinasDaTurma(turmaNome2):

                                        s =  solucao.trocaSlot((turmaNome1,i1,j1),(turmaNome2,i2,j2))

                                elif solucao.instancia.vaga(pivo1) and not solucao.instancia.vaga(pivo2):
                                    if pivo2[0] in solucao.instancia.nomesDisciplinasDaTurma(turmaNome1):

                                        s =  solucao.trocaSlot((turmaNome1,i1,j1),(turmaNome2,i2,j2))

                                if s is not None and s.valida():
                                    # print('2')
                                    yield s

def gerarVizinhoTTEP(solucao):
    for i,turmaNome1 in enumerate(solucao.instancia.turmas[0:-1]):
        for turmaNome2 in solucao.instancia.turmas[i+1:]:

            for i,disciplina1 in enumerate(solucao.instancia.disciplinasDaTurma(turmaNome1)[0:-1]):
                for disciplina2 in solucao.instancia.disciplinasDaTurma(turmaNome2)[i+1:]:

                    if not solucao.instancia.vaga(disciplina1) and not solucao.instancia.vaga(disciplina2):
                        s = solucao.trocaProfessorEntreTurmas(turmaNome1,turmaNome2,disciplina1[0],disciplina2[0])
                        if s is not None and s.valida():
                            # print('3')
                            yield s

def gerarVizinhoTPD(solucao):
    for turmaNome in solucao.instancia.turmas:
        for disciplina in solucao.instancia.disciplinasDaTurma(turmaNome):
            if not solucao.instancia.vaga(disciplina):
                for professoresHabilitado in solucao.instancia.professoresHabilitados(disciplina):

                    s =  solucao.trocaProfessorDaDisciplinaNaTurma(turmaNome, disciplina[0], professoresHabilitado)
                    if s is not None and s.valida():
                        # print('4')
                        yield s
