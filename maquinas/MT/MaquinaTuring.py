import json
import copy
from maquinas.generic.machine import Machine

class TuringMachine(Machine):
    saida = []

    def _build_index_maps(self, states, tape_symbols):
        self.state_to_index = {s: i for i, s in enumerate(states)}
        self.index_to_state = {i: s for s, i in self.state_to_index.items()}

        self.symbol_to_index = {sym: i for i, sym in enumerate(tape_symbols)}
        self.index_to_symbol = {i: sym for sym, i in self.symbol_to_index.items()}

    def _parse_transition_function(self, tf_dict):
        # Obter todos os estados e símbolos a partir das transições e estados finais/rejeição
        states = set()
        symbols = set()

        # Primeiro, coletamos todos os estados e símbolos
        for key, value in tf_dict.items():
            k = key.strip("()")
            state_read, symbol_read = k.split(',')
            state_read = state_read.strip()
            symbol_read = symbol_read.strip()

            new_state, write_symbol, direction = value

            states.add(state_read)
            states.add(new_state)
            symbols.add(symbol_read)
            symbols.add(write_symbol)

        # Garantir que o símbolo branco esteja na lista de símbolos
        if self.blank_symbol not in symbols:
            symbols.add(self.blank_symbol)

        # Converter para lista para ter uma ordem definida
        states = sorted(states)
        symbols = sorted(symbols)

        # Construir mapas de índice
        self._build_index_maps(states, symbols)

        # Criar a matriz de transições: 
        # Para cada estado e símbolo, teremos (new_state, write_symbol, direction) ou None
        transition_matrix = [[None for _ in symbols] for _ in states]

        # Preencher a matriz de transições
        for key, value in tf_dict.items():
            k = key.strip("()")
            state_read, symbol_read = k.split(',')
            state_read = state_read.strip()
            symbol_read = symbol_read.strip()

            new_state, write_symbol, direction = value

            # Obter índices
            sr_i = self.state_to_index[state_read]
            sy_i = self.symbol_to_index[symbol_read]

            ns_i = self.state_to_index[new_state]
            ws_i = self.symbol_to_index[write_symbol]

            transition_matrix[sr_i][sy_i] = (ns_i, ws_i, direction)

        return states, symbols, transition_matrix


    def load_input(self, input_data):
        """
        Carrega a palavra de entrada na fita.
        """
        self.input_data = input_data
        self.tape = list(input_data if input_data else self.blank_symbol)
        self.head_position = 0
        # O estado atual agora é um índice
        self.current_state_index = self.state_to_index[self.initial_state]

    def step(self):
        """
        Executa um único passo da simulação.
        """
        if self.head_position < 0:
            self.tape.insert(0, self.blank_symbol)
            self.head_position = 0
        elif self.head_position >= len(self.tape):
            self.tape.append(self.blank_symbol)

        current_symbol = self.tape[self.head_position]
        # Obter índice do símbolo atual
        if current_symbol not in self.symbol_to_index:
            # Caso apareça um símbolo não conhecido, tratar como símbolo em branco ou erro
            symbol_index = self.symbol_to_index[self.blank_symbol]
        else:
            symbol_index = self.symbol_to_index[current_symbol]

        # Buscar transição na matriz
        transition = self.transition_matrix[self.current_state_index][symbol_index]

        if transition is not None:
            new_state_i, write_symbol_i, direction = transition
            # Aplicar transição
            self.tape[self.head_position] = self.index_to_symbol[write_symbol_i]
            self.current_state_index = new_state_i
            if direction == 'R':
                self.head_position += 1
            elif direction == 'L':
                self.head_position -= 1
            return True
        else:
            return False

    def is_accepting(self):
        """
        Verifica se o estado atual é um estado de aceitação.
        """
        return self.index_to_state[self.current_state_index] in self.final_states

    def is_rejecting(self):
        """
        Verifica se o estado atual é um estado de rejeição.
        """
        return self.index_to_state[self.current_state_index] in self.reject_states

    def reset(self):
        """
        Reinicia a máquina com o último dado de entrada carregado.
        """
        if self.input_data is not None:
            self.load_input(self.input_data)

    def get_config(self):
        """
        Retorna a configuração atual da máquina (estado, posição da cabeça, fita).
        """
        return {
            'current_state': self.index_to_state[self.current_state_index],
            'head_position': self.head_position,
            'tape': ''.join(self.tape)
        }

    def start(self, config, words):
        Json = json.loads(config)
        """
        Inicializa a Máquina de Turing a partir de um dicionário de configuração (JSON).
        """
        self.blank_symbol = Json.get('blank_symbol', '_')
        self.initial_state = Json.get('initial_state', 'q0')
        self.final_states = set(Json.get('final_states', []))
        self.reject_states = set(Json.get('reject_states', []))

        # Aqui é retornado (states, symbols, transition_matrix)
        states, symbols, self.transition_matrix = self._parse_transition_function(Json.get('transition_function', {}))

        # Agora "states" e "symbols" são armazenados caso necessário
        self.states = states
        self.symbols = symbols
        
        self.head_position = 0
        self.tape = []
        self.input_data = None
        
        output_log = {
            "machine_type": "turing",
            "words_log": []
        }

        self.reset()
        self.load_input(words)

        word_log = {
                "word": words,
                "steps": []
            }

        step_count = 0
        initial_config = self.get_config()
        word_log["steps"].append({
                "step": step_count,
                "state": initial_config["current_state"],
                "tape": initial_config["tape"],
                "head_position": initial_config["head_position"]
            })

        while not self.is_accepting() and not self.is_rejecting():
            successful_step = self.step()
            step_count += 1
            config = self.get_config()
            word_log["steps"].append({
                "step": step_count,
                "state": config["current_state"],
                "tape": config["tape"],
                "head_position": config["head_position"]
            })
            if not successful_step:
                break

        if self.is_accepting():
            result = "accepted"
        elif self.is_rejecting():
            result = "rejected"
        else:
            result = "halted_without_accept"

        word_log["result"] = result
        output_log["words_log"].append(word_log)

        self.saida = json.loads(json.dumps(output_log, indent=4, ensure_ascii=False))
