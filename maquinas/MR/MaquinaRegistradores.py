
import AbrirArquivo
import Estados
import Registradores

class MaquinaRegistradores():

    caminho_arquivo = 'input_mr.json'


    def start(caminho_arquivo):
    
        valorRegistradores, listaDeEstados = AbrirArquivo.AbrirArquivo.abrir(caminho_arquivo)

        print('\n \n'+ valorRegistradores + listaDeEstados + '\n\n')

        registradores = Registradores.Registradores(valorRegistradores)
        estados = Estados.Estados(listaDeEstados, registradores)



        print(" =========== TRANSIÇÕES: ===========\n")

        #print(estados.mostrar_estados())

        print(estados.start())


    start(caminho_arquivo)