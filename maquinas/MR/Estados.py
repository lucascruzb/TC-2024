import json

class Estados:
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


        output_mr = {
        "machineType": "RegisterMachine",
        "Estado Inicial Registradores": estadoInicialRegis,
        "Transicoes": transicoes
        }

        output_mr_str = json.dumps(output_mr)

        with open("output_mr.json", "w",encoding="utf-8") as f:
            json.dump(output_mr, f, indent=4, ensure_ascii=False)

        return estadoInicialRegis + "\n" + transicoes

