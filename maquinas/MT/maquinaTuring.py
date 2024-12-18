import json
import copy
from maquinas.generic.machine import Machine

class TuringMachine(Machine):
    saida = []

    def _parse_transition_function(self, tf_dict):
        parsed = {}
        for key, value in tf_dict.items():
            k = key.strip("()")
            state_read, symbol_read = k.split(',')
            state_read = state_read.strip()
            symbol_read = symbol_read.strip()

            new_state, write_symbol, direction = value
            parsed[(state_read, symbol_read)] = (new_state, write_symbol, direction)
        return parsed

    def load_input(self, input_data):
        """
        Carrega a palavra de entrada na fita.
        """
        self.input_data = input_data
        self.tape = list(input_data if input_data else self.blank_symbol)
        self.head_position = 0
        self.current_state = self.current_state

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
        key = (self.current_state, current_symbol)

        if key in self.transition_function:
            new_state, write_symbol, direction = self.transition_function[key]
            self.tape[self.head_position] = write_symbol
            self.current_state = new_state
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
        return self.current_state in self.final_states

    def is_rejecting(self):
        """
        Verifica se o estado atual é um estado de rejeição.
        """
        return self.current_state in self.reject_states

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
            'current_state': self.current_state,
            'head_position': self.head_position,
            'tape': ''.join(self.tape)
        }

    def start(self,config, words):

        Json = json.loads(config)
        """
        Inicializa a Máquina de Turing a partir de um dicionário de configuração (JSON).
        """
        self.blank_symbol = Json.get('blank_symbol', '_')
        self.current_state = Json.get('initial_state', 'q0')
        self.final_states = set(Json.get('final_states', []))
        self.reject_states = set(Json.get('reject_states', []))
        self.transition_function = self._parse_transition_function(Json.get('transition_function', {}))
        self.head_position = 0
        self.tape = []
        self.input_data = None
        
        """
        Executa a simulação para uma lista de palavras.

        :param words: Lista de palavras para processar.
        :return: Log da execução contendo os resultados.
        """
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
