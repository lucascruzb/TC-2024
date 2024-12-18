import json
import sys
from collections import deque
from maquinas.generic.machine import Machine

class AutomatoDeFila(Machine):
    saida = []

    def start(self, arquivo_console, entrada):
        # Validar e carregar o autômato
        automaton_definition = json.loads(arquivo_console)

        # Validar se o autômato é válido
        machine_type = self.validate_automaton(automaton_definition)

        # Criar matriz de transições
        self.matrix, self.state_to_index, self.symbol_to_index = self.create_transition_matrix(automaton_definition)

        # Validar a entrada
        self.validate_input(entrada, automaton_definition['alphabet'])

        # Processar a entrada no autômato
        result, transitions = self.process_input_with_matrix(automaton_definition, entrada)

        # Registrar transições realizadas
        for transition in transitions:
            self.saida.append(f"δ({transition['current_state']}, {transition['input_symbol']}, {transition['output_symbol']}, {transition['final_fila']}) → {transition['next_state']}")

    def validate_automaton(self, automaton):
        # Valida se o autômato possui estados de aceitação ou rejeição
        has_accept_states = len(automaton.get('accept_states', [])) > 0
        has_reject_states = len(automaton.get('reject_states', [])) > 0

        if not has_accept_states:
            print("Erro: A máquina precisa ter pelo menos um estado de aceitação.")
            sys.exit(1)

        # Determinar o tipo de máquina
        if has_accept_states and has_reject_states:
            machine_type = "Máquina que Decide"
        elif has_accept_states and not has_reject_states:
            machine_type = "Máquina que Semidecide"
        else:
            machine_type = "Máquina Inválida"

        print(f"Tipo de Máquina: {machine_type}")
        return machine_type

    def validate_input(self, input_string, alphabet):
        # Valida se a entrada está no formato correto
        if not input_string:
            print("Erro: A entrada está vazia. Deve conter pelo menos o símbolo '#'.")
            sys.exit(1)

        for char in input_string:
            if char not in alphabet:
                print(f"Erro: O símbolo '{char}' na entrada não faz parte do alfabeto {alphabet}.")
                sys.exit(1)

        if '#' not in input_string:
            print("Erro: A entrada deve conter pelo menos um '#'.")
            sys.exit(1)

        if not input_string.endswith('#'):
            print("Erro: A entrada deve terminar com '#'.")
            sys.exit(1)

        print("Entrada validada: contém '#' e todos os símbolos pertencem ao alfabeto.")

    def create_transition_matrix(self, automaton):
        # Cria a matriz de transições a partir da definição do autômato
        states = automaton['K']
        alphabet = automaton['alphabet']

        # Mapear estados e símbolos para índices
        state_to_index = {state: i for i, state in enumerate(states)}
        symbol_to_index = {symbol: i for i, symbol in enumerate(alphabet)}

        # Inicializar a matriz com vazio
        matrix = [[None for _ in alphabet] for _ in states]

        # Preencher a matriz com as transições
        for state, transitions in automaton['transitions'].items():
            for symbol, transition in transitions.items():
                row = state_to_index[state]
                col = symbol_to_index[symbol]
                matrix[row][col] = tuple(transition)

        return matrix, state_to_index, symbol_to_index

    def process_input_with_matrix(self, automaton, input_string):
        # Processa a entrada usando a matriz de transições
        current_state = automaton['start_state']
        current_state_index = self.state_to_index[current_state]
        queue = deque(input_string)
        transitions_log = []  # Armazena as transições realizadas

        print("\n=== Execução da Máquina ===")
        print(f"{'Palavra Atual':<20} {'Estado Atual':<15} {'Símbolo Consumido':<20} {'Próximo Estado':<15}")
        print("=" * 70)

        while queue:
            current_symbol = queue.popleft()  # Consome o símbolo da fila

            # Verificar se o símbolo pertence ao alfabeto
            if current_symbol not in self.symbol_to_index:
                raise ValueError(f"Símbolo inválido: {current_symbol}")

            # Obter a transição da matriz
            col = self.symbol_to_index[current_symbol]
            transition = self.matrix[current_state_index][col]

            if transition is None:
                print("Erro: Transição não definida para o estado atual e símbolo consumido.")
                return "Palavra Não Reconhecida", transitions_log

            # Extrair os dados da transição
            output_symbol, final_fila, next_state = transition
            next_state_index = self.state_to_index[next_state]

            # Registrar a transição
            transitions_log.append({
                "current_state": current_state,
                "input_symbol": current_symbol,
                "output_symbol": output_symbol,
                "next_state": next_state,
                "final_fila": final_fila
            })

            # Exibir a transição no terminal
            current_word = ''.join(queue)
            print(f"{current_word:<20} {current_state:<15} {current_symbol:<20} {next_state:<15}")

            # Atualizar o estado atual e adicionar ao final da fila, se necessário
            current_state = next_state
            current_state_index = next_state_index
            if final_fila != "e":  # "e" indica que nada será adicionado
                queue.append(final_fila)

            # Verificar se o estado atual é de rejeição
            if current_state in automaton['reject_states']:
                print("=== Palavra Rejeitada: O autômato atingiu um estado de rejeição ===")
                return "Palavra Rejeitada", transitions_log

        print("=" * 70)

        # Verificar se terminou em um estado de aceitação
        if current_state in automaton['accept_states']:
            print("=== Palavra Aceita ===")
            return "Palavra Aceita", transitions_log
        else:
            print("=== Palavra Não Reconhecida ===")
            return "Palavra Não Reconhecida", transitions_log
