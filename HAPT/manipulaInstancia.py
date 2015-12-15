'''
@author: leo
'''
matrizDePreferenciasPath = 'dataset/preferenciasProfessorHorario'
disciplinasPorTurmasPath = 'dataset/disciplinasPorTurmas'
disciplinasHabilitadasPath = 'dataset/disciplinasHabilitadas'

from problema import *
from metaheuristicas import GRASP_VND

class Instancia(object):
    '''
    Representa os dados da instancia, os extraindo dos arquivos txt
    '''
    
    def __init__(self):
        '''
        Inicia oobjeto e carrega os daos nos arquivos
        '''
        self.disciplinasPorTurmas = {}
        self.disciplinasDoProfessori = []
        self.preferenciasDoProfessori = []
        
        self._carregaArquivos()
        
    @property
    def turmas(self):
        return list(sorted(self.disciplinasPorTurmas.keys()))
    
    @property
    def disciplinas(self):
        return sorted([val for sublist in self.disciplinasPorTurmas.values() for val in sublist])[0:-6]
    
    def vaga(self,disciplina):
        return disciplina[0] == 'VAGA'
    
    def vagaNome(self,disciplinaNome):
        return disciplinaNome == 'VAGA'
    
    def getPreferencia(self,professor,tempo,dia):
        return int(self.preferenciasDoProfessori[professor][dia][tempo])

    def disciplinasDaTurma(self,turma):
        return list(sorted(self.disciplinasPorTurmas[turma]))
    
    def nomesDisciplinasDaTurma(self,turma):
        return sorted([n for (n,c) in self.disciplinasPorTurmas[turma]])
    
    def professoresHabilitados(self,disciplina):
        professoresHabilitados = []
        if disciplina[0] == 'VAGA':
            professoresHabilitados.append(None)
        else:
            for i,disciplinas in enumerate(self.disciplinasDoProfessori):
                if disciplina[0] in disciplinas:
                    professoresHabilitados.append(i)
            
        return sorted(professoresHabilitados)
    
    def professoresHabilitadosDisciplinaNome(self,disciplinaNome):
        professoresHabilitados = []
        
        if disciplinaNome == 'VAGA':
            professoresHabilitados.append(None)
        else:
            for i,disciplinas in enumerate(self.disciplinasDoProfessori):
                if disciplinaNome in disciplinas:
                    professoresHabilitados.append(i)
            
        return sorted(professoresHabilitados)
    
    @property
    def turmaDisciplinaToCargaDic(self):
        turmaDisciplinaToCargaDic = {}
        for turma in self.turmas:
            for disciplinaDaTurma in self.disciplinasDaTurma(turma):
                turmaDisciplinaToCargaDic[turma,disciplinaDaTurma[0]] = int(disciplinaDaTurma[1])
                
        return turmaDisciplinaToCargaDic
    
    def _carregaArquivos(self):
        with open(disciplinasPorTurmasPath, encoding='utf-8', newline='\n') as disciplinasPorTurmas:
            turma = ''
            for linha in disciplinasPorTurmas:
                if linha.strip()[0] == '=':
                    turma = linha[1:-1]
                    self.disciplinasPorTurmas[turma] = []
                else:
                    linha = linha.strip().split()
                    self.disciplinasPorTurmas[turma].append((linha[0],linha[1]))
 
        with open(disciplinasHabilitadasPath, encoding='utf-8', newline='\n') as disciplinasHabilitadasPorProfessor:
            for disciplinasDoProfessori in disciplinasHabilitadasPorProfessor:    
                disciplinasDoProfessori = disciplinasDoProfessori.split()
#                 disciplinasDoProfessori.append('VAGA')
                self.disciplinasDoProfessori.append(disciplinasDoProfessori)
                  
        with open(matrizDePreferenciasPath, encoding='utf-8', newline='\n') as preferenciasProfessorHorario:
            for preferenciasDoProfessori in preferenciasProfessorHorario:    
                preferenciasDoProfessori = preferenciasDoProfessori.strip().split()
                
                if len(preferenciasDoProfessori) > 0:
                    preferenciasDoProfessoriTuplas = []
                    
                    for i,p in enumerate(preferenciasDoProfessori):
                        if i%2 == 0:
                            tupla = (p,None)
                        else:
                            tupla = (tupla[0],p)
                            preferenciasDoProfessoriTuplas.append(tupla)
                    
                    self.preferenciasDoProfessori.append(preferenciasDoProfessoriTuplas)            
                       
if __name__ == '__main__':
    instancia = Instancia()
    
#     print(instancia.turmas,"\n")
#     
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
     
#     solucao = Solucao(instancia) 
#     carregaTeste(solucao)
#     solucao.printSolucao()
    
#     solucao = GRASP_VND(5,instancia,0)     
#     solucao.printSolucao()
#
#     solucao = GRASP_VND(50,instancia,0.25)     
#     solucao.printSolucao()

#     solucao = GRASP_VND(50,instancia,0.5)     
#     solucao.printSolucao()
     
#     solucao = GRASP_VND(50,instancia,0.75)     
#     solucao.printSolucao()  

    solucao = GRASP_VND(50,instancia,1)     
    solucao.printSolucao()
 
#     solucao = GRASP_VND(50,instancia,0.6)     
#     solucao.printSolucao()

#     solucao = GRASP_VND(50,instancia,0.7)     
#     solucao.printSolucao()

#     solucao = GRASP_VND(50,instancia,0.8)     
#     solucao.printSolucao()

#     geradorteste = gerarVizinhoTHPDD(solucao)
#     i = 0
#     for s in geradorteste:
#         i+=1
#         if i >= 1 and i<= 3: s.printSolucao()
#         if i == 1: s.printSolucao()

                    
                    
                    
                    
                    
    