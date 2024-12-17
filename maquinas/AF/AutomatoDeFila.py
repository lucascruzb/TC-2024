import json
import sys
from maquinas.generic.machine import Machine

class AutomatoDeFila(Machine):
    saida =[]

    def start(self, arquivo_console, entrada): 

        # Caminho para o arquivo JSON de saída das transições
        output_transitions_file = "transitions_log.json"

        # Validar se o autômato é uma máquina de fila válida
        machine_type = self.validate_automaton(json.loads(arquivo_console))
        automaton_definition = json.loads(arquivo_console)

        # Validar a entrada
        self.validate_input(entrada, automaton_definition['alphabet'])

        # Processar a entrada no autômato
        result, transitions = self.process_input(automaton_definition, entrada)

        # Imprimir o resultado e as transições realizada

        for transition in transitions:
            self.saida.append(f"δ({transition['current_state']}, {transition['input_symbol']}, {transition['output_symbol']}, {transition['final_fila']}) → {transition['next_state']}")

    def load_automaton(self, file_path):
        #loud
        with open(file_path, 'r') as file:
            automaton = json.load(file)
        return automaton

    def validate_automaton(self, automaton):
        #valida automato
        has_accept_states = len(automaton.get('accept_states', [])) > 0
        has_reject_states = len(automaton.get('reject_states', [])) > 0

        if not has_accept_states:
            print("Erro: A máquina precisa ter pelo menos um estado de aceitação.")
            sys.exit(1)

        # Determina o tipo de máquina
        if has_accept_states and has_reject_states:
            machine_type = "Máquina que Decide"
        elif has_accept_states and not has_reject_states:
            machine_type = "Máquina que Semidecide"
        else:
            machine_type = "Máquina Inválida"

        print(f"Tipo de Máquina: {machine_type}")
        return machine_type

    def validate_input(self, input_string, alphabet):
        #valida input
        if not input_string:
            print("Erro: A entrada está vazia. Deve conter pelo menos o símbolo '#'.")
            sys.exit(1)

        # Verifica se todos os caracteres da entrada estão no alfabeto
        for char in input_string:
            if char not in alphabet:
                print(f"Erro: O símbolo '{char}' na entrada não faz parte do alfabeto {alphabet}.")
                sys.exit(1)

        # Verifica se a entrada contém pelo menos um '#' e termina com '#'
        if '#' not in input_string:
            print("Erro: A entrada deve conter pelo menos um '#'.")
            sys.exit(1)
        if not input_string.endswith('#'):
            print("Erro: A entrada deve terminar com '#'.")
            sys.exit(1)

        print("Entrada validada: contém '#' e todos os símbolos pertencem ao alfabeto.")

    def process_input(self, automaton, input_string):
    
        current_state = automaton['start_state']
        queue = list(input_string)
        transitions_log = []  # Lista para armazenar todas as transições realizadas

        print("\n=== Execução da Máquina ===")
        print(f"{'Palavra Atual':<20} {'Estado Atual':<15} {'Símbolo Consumido':<20} {'Próximo Estado':<15}")
        print("=" * 70)

        while queue:
            current_symbol = queue.pop(0)  # Pega o símbolo na frente da fila

            if current_symbol not in automaton['alphabet']:
                raise ValueError(f"Símbolo inválido: {current_symbol}")

            # Obter a transição para o estado atual e símbolo atual
            if current_symbol in automaton['transitions'].get(current_state, {}):
                output_symbol, final_fila, next_state = automaton['transitions'][current_state][current_symbol]
                transitions_log.append({
                    "current_state": current_state,
                    "input_symbol": current_symbol,
                    "output_symbol": output_symbol,
                    "next_state": next_state,
                    "final_fila": final_fila
                })

                # Mostrar no terminal a palavra atual, estado atual e próximo estado
                current_word = ''.join(queue)
                print(f"{current_word:<20} {current_state:<15} {current_symbol:<20} {next_state:<15}")

                # Atualizar estado e adicionar ao final da fila, se necessário
                current_state = next_state
                if final_fila != "e":  # "e" indica que nada será adicionado
                    queue.append(final_fila)
            else:
                print("Erro: Transição não definida para o estado atual e símbolo consumido.")
                return "Palavra Não Reconhecida", transitions_log

            # Se atingir um estado de rejeição, parar imediatamente
            if current_state in automaton['reject_states']:
                print("=== Palavra Rejeitada: O autômato atingiu um estado de rejeição ===")
                return "Palavra Rejeitada", transitions_log

        print("=" * 70)

        # Verificar se terminou corretamente
        if current_state in automaton['accept_states']:
            print("=== Palavra Aceita ===")
            return "Palavra Aceita", transitions_log
        else:
            print("=== Palavra Não Reconhecida ===")
            return "Palavra Não Reconhecida", transitions_log
        #save
    
  # def save_transitions_to_json(self, transitions, output_file):
   #     """Salva as transições realizadas em um arquivo JSON."""
    #    with open(output_file, 'w') as file:
     #       json.dump(transitions, file, indent=4)