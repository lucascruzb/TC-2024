from maquinas.machine import Machine
import copy
import json
import re

class MaquinaRegistradores(Machine):
    saida =[]
    #entrada = "A=10,B=2,C=0"

    def start(self, arquivo_console, entrada): #se for do console receber um True em console

        #arquivo_console = "-B,2,4\n+A,3\n+C,1\n-C,5,#\n+B,4" # substituir pelo retorno do console
        valorRegistradores, listaDeEstados = self.abrir(arquivo_console,entrada)

        registradores = Registradores(valorRegistradores)
        estados = Estados(listaDeEstados, registradores)

        self.saida = estados.start().split("\n")

    def abrir(self, console,entrada):
        registradores = ""
        estados = ""
        conteudoConsole = json.loads(console)

        linhasConsole = entrada
        linhasConsole = linhasConsole + "\n" + "\n".join(conteudoConsole["states"])
        linhasConsole = linhasConsole.splitlines()

        primeiraLinha = True

        for linhaConsole in linhasConsole:
            linhaConsole = linhaConsole.strip()  # Remove quebras de linha e espaço
            
            if primeiraLinha:
                padraoCorretoRegistradores = r'^([a-z]=\d+)(,[a-z]=\d+)*$'

                # Verifica se a linha corresponde ao padrão
                if re.fullmatch(padraoCorretoRegistradores, linhaConsole, re.IGNORECASE):
                    #print("A primeira linha está no formato correto.")
                    registradores = linhaConsole + "\n"
                else:
                    return "ERRO A primeira linha não está no formato esperado.", " "

            else:
                padraoCorretoEstados = r"^[\+\-][a-zA-Z](,\d+)*(,?#)?$"
                if re.fullmatch(padraoCorretoEstados, linhaConsole, re.IGNORECASE):
                    #print("Verificada: " + linha)
                    estados = estados + linhaConsole + "\n"
                else:
                        return "ERRO Descrição de estado incorreto" , " "
            
            primeiraLinha = False

        return registradores, estados
    
class Estados:
    saida =[]

    def __init__(self, estados_lista, registradores):
        self.estados = estados_lista
        self.registradores = registradores

    def mostrar_estados(self):
        return self.estados
    
    def start(self):

        estadoInicialRegis = self.registradores.mostrar_registradores()
        transicoes = ""

        listaDeEstados = self.estados.splitlines()
        numero_de_estados = len(listaDeEstados)
        estadoAtual = 0
        estadoFinal = "0"


        while estadoFinal != "#":
           
            linha = listaDeEstados[estadoAtual]
            registrador = linha[1]
            oprecao = linha[0]

            if oprecao == "+":
                self.registradores.acrescer(registrador)
                estadoAtual = int(linha[3])-1

                linhaAux = listaDeEstados[int(estadoAtual)]
                proxEstado = linhaAux[0] + linhaAux[1]
                transicoes = transicoes + "Trasicao: " + oprecao + registrador + " -> " + proxEstado
                transicoes = transicoes + "  Registradores: " +  self.registradores.mostrar_registradores() + "\n"

            else :
                deuParadecrementar = self.registradores.decrementar(registrador)
                if deuParadecrementar == 1:
                    estadoAtual = int(linha[3])-1

                    linhaAux = listaDeEstados[estadoAtual]
                    proxEstado = linhaAux[0] + linhaAux[1]
                    transicoes = transicoes + "Trasicao: " + oprecao + registrador + " -> " + proxEstado
                    transicoes = transicoes + "  Registradores: " +  self.registradores.mostrar_registradores() + "\n"
                    
                else:
                    estadoAtual = linha[5]

                    if estadoAtual == "#":
                        estadoFinal = linha[5]
                        transicoes = transicoes + "Trasicao: " + oprecao + registrador + " -> " + estadoFinal + " "
                        transicoes = transicoes + "  Registradores: " +  self.registradores.mostrar_registradores() + "\n"

                    else:
                        estadoAtual = int(linha[5])-1
                        linhaAux = listaDeEstados[estadoAtual]
                        proxEstado = linhaAux[0] + linhaAux[1]
                        transicoes = transicoes + "Trasicao: " + oprecao + registrador + " -> " + proxEstado
                        transicoes = transicoes + "  Registradores: " +  self.registradores.mostrar_registradores() + "\n"
        
        #print(transicoes)

        return transicoes

class Registradores:
    def __init__(self, registradores_str):
        # Quebra a string de registradores em um formato "A=3, B=2, C=0"
        registradores_list = registradores_str.split(",")
        
        # Para cada registrador na lista, cria um atributo para cada letra
        for item in registradores_list:
            letra, valor = item.split("=")
            valor = int(valor)  # Converte o valor para inteiro
            setattr(self, letra, valor)  # Cria o atributo dinamicamente

    def mostrar_registradores(self):
        # Cria uma lista de strings no formato 'A=3', 'B=2', etc.
        registradores_formatados = [f"{atributo}={getattr(self, atributo)}" for atributo in self.__dict__]
        # Junta os registradores com | entre eles e retorna a string
        return " | ".join(registradores_formatados)
    
    def decrementar(self, registrador):
        # Verifica se o registrador existe e se o valor é maior que 0
        if hasattr(self, registrador):
            if getattr(self, registrador) > 0:
                setattr(self, registrador, getattr(self, registrador) - 1)
                #print(f"{registrador} decrementado com sucesso! Novo valor: {getattr(self, registrador)}")
                return 1
            else:
                #print(f"Não foi possível decrementar {registrador}, valor já está em 0.")
                return 0
        else:
            #print(f"O registrador {registrador} não existe.")
            return 0

    def acrescer(self, registrador):
        # Verifica se o registrador existe e acrescenta o valor
        if hasattr(self, registrador):
            setattr(self, registrador, getattr(self, registrador) + 1)
            #print(f"{registrador} acrescido com sucesso! Novo valor: {getattr(self, registrador)}")
            return 1
        else:
            #print(f"O registrador {registrador} não existe.")
            return 0
