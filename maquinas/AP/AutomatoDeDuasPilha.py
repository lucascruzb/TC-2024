import json
from maquinas.machine import Machine
import copy

# ===========================================
# Implementação Máquina de Autômatos de Duas Pilhas
# Execução: Execute esse script utilizando um arquivo JSON como argumento na linha de comando
# Exemplo: python duas_pilhas.py automato.json
# ============================================

class AutomatoDeDuasPilha(Machine) :
    saida = []

    def automaton_compute(self, entrada ,states, stack_symbols, initial_state, final_states, transitions):
        
        while True:
            stack1 = []  # Pilha 1
            stack2 = []  # Pilha 2
            current_state = initial_state


            input_buffer = list(entrada)  # Buffer de entrada como lista de caracteres

            while True:
                self.salvar_transicao(current_state,input_buffer , stack1, stack2)

                if current_state in final_states:
                    print("\nA cadeia foi aceita!")
                    break

                if current_state not in transitions:
                    print("\nA cadeia foi rejeitada: estado sem transições.")
                    break

                symbol = input_buffer.pop(0) if input_buffer else "<vazio>"
            
                if symbol not in transitions[current_state]:
                    print("\nA cadeia foi rejeitada: transição não encontrada.")
                    break

                transition = transitions[current_state][symbol]

                next_state = transition['next_state']
                stack1_action = transition['stack1']
                stack2_action = transition['stack2']

                # Processar ações na pilha 1
                if stack1_action == "pop" and stack1:
                    stack1.pop()
                elif stack1_action.startswith("push"):
                    _, value = stack1_action.split()
                    stack1.append(value)

                # Processar ações na pilha 2
                if stack2_action == "pop" and stack2:
                    stack2.pop()
                elif stack2_action.startswith("push"):
                    _, value = stack2_action.split()
                    stack2.append(value)

                current_state = next_state

                if not input_buffer and current_state in final_states:
                    print("\nA cadeia foi aceita!")
                    break
            break

    def start(self, Json, Entrada):
        data = json.loads(Json)
        try:
            states = data['states']
            stack_symbols = data['stack_symbols']
            initial_state = data['initial_state']
            final_states = data['final_states']
            transitions = data['transitions']

        except KeyError as err:
            print(f'O arquivo JSON não contém todos os elementos necessários: {err}')
            raise SystemExit()

        print('--------------------')
        print(f'Estados: {states}')
        print(f'Símbolos das pilhas: {stack_symbols}')
        print(f'Estado inicial: {initial_state}')
        print(f'Estados finais: {final_states}')
        print(f'Transições: {json.dumps(transitions, indent=4)}')
        print('--------------------')

        self.automaton_compute(Entrada,states, stack_symbols, initial_state, final_states, transitions)

    def read_json(self,filename):
        with open(filename, 'r') as f:
            if not filename.lower().endswith('.json'):
                print('O arquivo inserido precisa ser do formato JSON.')
                raise SystemExit()
            else:
                data = json.load(f)
        return data

    def salvar_transicao(self,current_state,input_buffer ,stack1, stack2):
        estado_json = {
            "estado_atual": current_state,
            "buffer_entrada": input_buffer ,
            "pilhas": {
                "pilha1": stack1 ,
                "pilha2": stack2 
        }   
    }
        self.saida.append(copy.deepcopy(estado_json))