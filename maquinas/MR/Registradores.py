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


