import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QFileDialog,
    QTextEdit, QComboBox, QPushButton, QProgressBar, QLabel, QSplitter
)
from PyQt5.QtCore import Qt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Simulador.Simulador import MachineSimulator
from maquinas.AP.AutomatoDeDuasPilha import AutomatoDeDuasPilha
from maquinas.MR.MaquinaRegistradores import MaquinaRegistradores
from maquinas.AF.AutomatoDeFila import AutomatoDeFila
from maquinas.MT.MaquinaTuring import TuringMachine



class SimuladorUI(QMainWindow):
    interacoes = 0
    saida = []
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #FFFFFF; color: black;")

        # Layout principal
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # Splitter principal
        splitter = QSplitter(Qt.Horizontal)

        # Área de Programação (Esquerda)
        self.programacao_area = QTextEdit()
        self.programacao_area.setPlaceholderText("Programação")
        splitter.addWidget(self.programacao_area)

        # Área de Simulação (Direita)
        self.simulacao_area = QTextEdit()
        self.simulacao_area.setReadOnly(True)
        self.simulacao_area.setPlaceholderText("Simulação")
        splitter.addWidget(self.simulacao_area)

        # Ajustar proporção do splitter
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        # Entrada e Controles Inferiores
        bottom_layout = QHBoxLayout()

        # Entrada
        self.entrada_label = QLabel("Entrada:")
        self.entrada_field = QTextEdit()
        self.entrada_field.setFixedHeight(40)
        bottom_layout.addWidget(self.entrada_label)
        bottom_layout.addWidget(self.entrada_field)

        # Botões e Controles
        self.maquina_combo = QComboBox()
        self.maquina_combo.setPlaceholderText("Selecionar máquina")
        self.maquina_combo.addItems(["Máquina de Turing","Autômato de duas pilhas","Autômato de fila","Máquina de registradores"])


        self.carregar_button = QPushButton("Carregar Programação")
        self.carregar_button.clicked.connect(self.abrir_json)

        self.salvar_button = QPushButton("💾")


        bottom_layout.addWidget(self.maquina_combo)
        bottom_layout.addWidget(self.carregar_button)
        bottom_layout.addWidget(self.salvar_button)

        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: lightgray;  /* Fundo cinza */
                border: 1px solid #000;       /* Borda preta */
                height: 20px;                 /* Altura da barra */
                text-align: center;           /* Texto no centro */
            }
            QProgressBar::chunk {
                background-color: gray;      /* Cor do carregamento */
            }
        """)
        self.progress_bar.setValue(0)

        # Botões de Simulação
        buttons_layout = QHBoxLayout()
        self.play_button = QPushButton("▶")
        self.stop_button = QPushButton("■")
        self.next_button = QPushButton("➤")
        buttons_layout.addWidget(self.progress_bar)
        buttons_layout.addWidget(self.stop_button)
        buttons_layout.addWidget(self.play_button)
        buttons_layout.addWidget(self.next_button)

        # Adicionar widgets ao layout principal
        main_layout.addWidget(splitter)
        main_layout.addLayout(bottom_layout)
        main_layout.addLayout(buttons_layout)

        # Configurar widget central
        self.setCentralWidget(main_widget)
        # Valor inicial do progresso
        self.progress_value = 0

        #conectar QComboBox
        self.maquina_combo.currentTextChanged.connect(self.setarMaquina)

        # Conectar botões
        self.next_button.clicked.connect(self.processar_entradas)
        self.play_button.clicked.connect(self.increment_progress)
        self.stop_button.clicked.connect(self.reset_progress)
        self.salvar_button.clicked.connect(self.salvar_maquina)

    def setarMaquina(self, nomeMaquina):
        self.maquina_combo.setCurrentText(nomeMaquina)

    def iniciarMaquina(self):
        simulator = MachineSimulator()
        tipoMaquina = self.maquina_combo.currentText()
        Json = self.programacao_area.toPlainText()
        Entrada = self.entrada_field.toPlainText()

        if tipoMaquina == "Autômato de duas pilhas" :
            AP = AutomatoDeDuasPilha("Autômato de duas pilhas")
            simulator.execute_machine(AP, Json, Entrada)
            return AP.saida
        if tipoMaquina == "Máquina de Turing":
            TM = TuringMachine("Máquina de Turing")
            simulator.execute_machine(TM, Json, Entrada)
            return TM.saida["words_log"][0]["steps"]
        if tipoMaquina == "Autômato de fila" :
            AF = AutomatoDeFila("Autômato de fila")
            simulator.execute_machine(AF, Json, Entrada)
            return AF.saida
        if tipoMaquina == "Máquina de registradores":
            MR = MaquinaRegistradores("Máquina de registradores")
            simulator.execute_machine(MR, Json, Entrada)
            MR.saida.pop(len(MR.saida) -1)
            return MR.saida

    def increment_progress(self):
        if self.progress_value == 0 :
            self.saida = self.iniciarMaquina()
            self.interacoes = 0
        """Incrementa o progresso ao clicar no botão Play."""
        if self.progress_value < 100:
            self.interacoes += 1
            self.progress_value = int((self.interacoes/len(self.saida))*100)
            self.progress_bar.setValue(self.progress_value )

            if self.maquina_combo.currentText() == "Autômato de duas pilhas" :
                self.simulacao_area.append(self.formatar_json(self.saida[self.interacoes-1]))
            elif self.maquina_combo.currentText() == "Máquina de Turing":
                self.simulacao_area.append(json.dumps(self.saida[self.interacoes-1]))
            elif self.maquina_combo.currentText() == "Autômato de fila" :
                self.simulacao_area.append(self.saida[self.interacoes-1])
            elif self.maquina_combo.currentText() == "Máquina de registradores":
                self.simulacao_area.append(self.saida[self.interacoes-1])
    
    def processar_entradas(self):
        if self.progress_value == 0 :
            self.saida = self.iniciarMaquina()
            self.interacoes = 1
            while self.interacoes < len(self.saida)+1 :
                if self.maquina_combo.currentText() == "Autômato de duas pilhas" :
                    self.simulacao_area.append(self.formatar_json(self.saida[self.interacoes-1]))
                elif self.maquina_combo.currentText() == "Máquina de Turing":
                    self.simulacao_area.append(json.dumps(self.saida[self.interacoes-1]))
                elif self.maquina_combo.currentText() == "Autômato de fila" :
                    self.simulacao_area.append(self.saida[self.interacoes-1])
                elif self.maquina_combo.currentText() == "Máquina de registradores":
                    self.simulacao_area.append(self.saida[self.interacoes-1])
                self.interacoes += 1
            self.progress_bar.setValue(100)
        elif self.progress_value < 100:
            self.interacoes += 1
            while self.interacoes < len(self.saida)+1 :
                if self.maquina_combo.currentText() == "Autômato de duas pilhas" :
                    self.simulacao_area.append(self.formatar_json(self.saida[self.interacoes-1]))
                elif self.maquina_combo.currentText() == "Máquina de Turing":
                    self.simulacao_area.append(json.dumps(self.saida[self.interacoes-1]))
                elif self.maquina_combo.currentText() == "Autômato de fila" :
                    self.simulacao_area.append(self.saida[self.interacoes-1])
                elif self.maquina_combo.currentText() == "Máquina de registradores":
                    self.simulacao_area.append(self.saida[self.interacoes-1])
                self.interacoes += 1
            self.progress_bar.setValue(100)
        
    def salvar_maquina(self):
        output_log = self.programacao_area.toPlainText()
        with open("resources/config.json", "w", encoding="utf-8") as f:
            json.dump(output_log, f, indent=4, ensure_ascii=False)

    def abrir_json(self):
        # Abrir uma janela para selecionar o arquivo JSON
        options = QFileDialog.Options()
        caminho, _ = QFileDialog.getOpenFileName(self, "Selecione o arquivo JSON", "", "Arquivos JSON (*.json);;Todos os Arquivos (*)", options=options)
        
        if caminho:
            try:
                # Ler o conteúdo do arquivo JSON
                with open(caminho, 'r', encoding='utf-8') as arquivo:
                    dados = json.load(arquivo)
                
                # Exibir o conteúdo do JSON na área de texto
                self.programacao_area.setText(json.dumps(dados, indent=4, ensure_ascii=False))
            except json.JSONDecodeError:
                self.programacao_area.setText("Erro: O arquivo selecionado não é um JSON válido.")

    def formatar_json(self, json_data):
        estado_atual = json_data["estado_atual"]
        proximo_estado = json_data["proximo_estado"]
        buffer_entrada = json_data["buffer_entrada"] 
        pilha1 = json_data["pilhas"]["pilha1"] 
        pilha2 = json_data["pilhas"]["pilha2"] 

        texto_formatado = (
        f"Estado Atual: {estado_atual}\n"
        f"Proximo Estado: {proximo_estado}\n"
        f"Buffer de Entrada: {buffer_entrada}\n\n"
        "Pilhas Atuais:\n"
        f"Pilha 1: {pilha1}\n"
        f"Pilha 2: {pilha2}\n"
        "=============================="
        )

        return texto_formatado
    
    def reset_progress(self):
        """Reseta o progresso da barra."""
        self.simulacao_area.clear()
        self.saida.clear()
        self.progress_value = 0
        self.progress_bar.setValue(0)

# Execução do aplicativo
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimuladorUI()
    window.show()
    sys.exit(app.exec_())
