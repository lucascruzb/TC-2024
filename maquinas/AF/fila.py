import json
import sys

def load_automaton(file_path):
    #LOUD
    with open(file_path, 'r') as file:
        automaton = json.load(file)
    return automaton

def validate_automaton(automaton):
    #valido automato
    for state in automaton['accept_states'] + automaton['reject_states']:
        valid = any(
            '#' in transitions and transitions['#'][0] == state
            for transitions in automaton['transitions'].values()
        )
        if not valid:
            print(f"Erro: O estado '{state}' não possui transição com '#' que o alcance.")
            sys.exit(1)  # Termina o programa imediatamente
    print("Autômato validado: é uma máquina de fila válida.")
    return True

def validate_input(input_string):
  #valida entrada
    if not input_string:
        print("Erro: A entrada está vazia. Deve conter pelo menos o símbolo '#'.")
        sys.exit(1)
    if '#' not in input_string:
        print("Erro: A entrada deve conter pelo menos um '#'.")
        sys.exit(1)
    if not input_string.endswith('#'):
        print("Erro: A entrada deve terminar com '#'.")
        sys.exit(1)
    print("Entrada validada: contém '#' e termina com '#'.")

def print_automaton_definition(automaton):
  #print
    print("=== Definição do Autômato ===")
    print(f"Estados (K): {', '.join(automaton['K'])}")
    print(f"Alfabeto (Γ): {', '.join(automaton['alphabet'])}")
    print("Transições (δ):")
    for state, transitions in automaton['transitions'].items():
        for symbol, (next_state, _) in transitions.items():
            print(f"  δ({state}, {symbol}) → {next_state}")
    print(f"Estado Inicial (s): {automaton['start_state']}")
    print(f"Estados de Aceitação (H): {', '.join(automaton['accept_states'])}")
    print(f"Estados de Rejeição: {', '.join(automaton['reject_states'])}")
    print("============================")

def process_input(automaton, input_string):
    #back
 
    current_state = automaton['start_state']
    queue = list(input_string)
    transitions_log = []  # Lista para armazenar todas as transições realizadas

    while queue:
        current_symbol = queue.pop(0)  # Pega o símbolo na frente da fila
        if current_symbol not in automaton['alphabet']:
            raise ValueError(f"Símbolo inválido: {current_symbol}")

        # Obter a transição para o estado atual e símbolo atual
        if current_symbol in automaton['transitions'][current_state]:
            next_state, _ = automaton['transitions'][current_state][current_symbol]
            transitions_log.append({
                "current_state": current_state,
                "symbol": current_symbol,
                "next_state": next_state
            })
            current_state = next_state
        else:
            raise ValueError(f"Transição não definida para estado {current_state} com símbolo {current_symbol}")

    # Verificar se terminou em estado de aceitação ou rejeição
    if current_state in automaton['accept_states']:
        return "Aceita", transitions_log
    elif current_state in automaton['reject_states']:
        return "Rejeita", transitions_log
    else:
        return "Estado final não reconhecido", transitions_log

def save_transitions_to_json(transitions, output_file):
    #SAVE
    with open(output_file, 'w') as file:
        json.dump(transitions, file, indent=4)

# Caminho para o arquivo JSON do autômato
json_file_path = "input_mr.json"

# Caminho para o arquivo JSON de saída das transições
output_transitions_file = "transitions_log.json"

# Carregar o autômato
automaton_definition = load_automaton(json_file_path)

# Validar se o autômato é uma máquina de fila válida
validate_automaton(automaton_definition)

# Entrada para testar
input_string = "0101010#"

# Validar a entrada
validate_input(input_string)

# Imprimir a definição do autômato
print_automaton_definition(automaton_definition)

# Processar a entrada no autômato
result, transitions = process_input(automaton_definition, input_string)

# Salvar as transições realizadas em um arquivo JSON
save_transitions_to_json(transitions, output_transitions_file)

# Imprimir o resultado e as transições realizadas
print(f"\nResultado para a entrada '{input_string}': {result}")
print("\n=== Transições Realizadas ===")
for transition in transitions:
    print(f"δ({transition['current_state']}, {transition['symbol']}) → {transition['next_state']}")
print("============================")

print(f"\nAs transições realizadas foram salvas no arquivo: {output_transitions_file}")
