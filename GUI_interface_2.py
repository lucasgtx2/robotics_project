import tkinter as tk
from tkinter import filedialog
import mido
from tkinter import ttk
import serial
from pyModbusTCP.server import ModbusServer
from time import sleep

SERVER_ADDRESS = '10.103.16.110' # IP do computador (servidor)
SERVER_PORT = 502

class PianoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Piano")

        self.teclas = []
        self.tecla_atual = ""
        self.sequencias = []
        self.escalas = []

        # Inicialização da comunicação serial com Arduino
        self.arduino = serial.Serial(port='COM7', baudrate=9600, timeout=1)

        self.criar_interface()

    def criar_interface(self):
        # Criação de botões brancos (teclas)
        notas_brancas = ["C", "D", "E", "F", "G", "A", "B", "NADA"]  # Adicionei "NADA"
        for nota in notas_brancas:
            if nota == "NADA":
                tecla = tk.Button(self.root, text=nota, command=lambda nota=nota: self.adicionar_tecla_pausa(nota), width=4, height=10, font=("Helvetica", 10, "bold"))
            else:
                tecla = tk.Button(self.root, text="", command=lambda nota=nota: self.adicionar_tecla(nota), width=4, height=10, bg="white")
            tecla.grid(row=0, column=notas_brancas.index(nota), padx=5, pady=5)
            self.teclas.append(tecla)

        # Criação de botões pretos (sustenidos)
        notas_pretas = ["J", "K", "L", "M", "N"]
        i = 0
        for nota in notas_pretas:
            tecla = tk.Button(self.root, text="", command=lambda nota=nota: self.adicionar_tecla(nota), bg="black", fg="white", width=2, height=6)
            if nota in ["J", "K"]:
                tecla.grid(row=0, column=i + 1, padx=5, pady=5)
                i += 1
            else:
                i += 1
                tecla.grid(row=0, column=i + 1, padx=5, pady=5)
            self.teclas.append(tecla)

        # Título "Digite o tempo"
        tempo_label = tk.Label(self.root, text="Digite o tempo")
        tempo_label.grid(row=1, column=0, padx=10, pady=5, columnspan=8)

        # Campo de entrada para o tempo
        self.tempo_entry = tk.Entry(self.root)
        self.tempo_entry.grid(row=2, column=0, padx=10, pady=5, columnspan=8)

        # Título "Digite a Escala (0:5)"
        escala_label = tk.Label(self.root, text="Escala (0:5)")
        escala_label.grid(row=3, column=0, padx=10, pady=5, columnspan=8)

        # Campo de entrada para a escala
        self.escala_entry = tk.Entry(self.root)
        self.escala_entry.grid(row=4, column=0, padx=10, pady=5, columnspan=8)

        # Botão para confirmar a sequência
        confirmar_botao = tk.Button(self.root, text="Confirmar", command=self.armazenar_sequencia)
        confirmar_botao.grid(row=5, column=0, padx=10, pady=10, columnspan=8)

        # Botão para enviar infos ao Arduino e ao UR
        send_button = tk.Button(self.root, text="Enviar", command=self.enviar)
        send_button.grid(row=6, column=0, padx=10, pady=10, columnspan=8)

        # Botão para limpar sequência
        confirmar_botao = tk.Button(self.root, text="Limpar sequência", command=self.limpar)
        confirmar_botao.grid(row=7, column=0, padx=10, pady=10, columnspan=8)

        # Título "Inserir música"
        escala_label = tk.Label(self.root, text="Inserir música")
        escala_label.grid(row=8, column=0, padx=10, pady=5, columnspan=8)

        # Campo de entrada para a música completa
        self.string_entry = tk.Entry(self.root)
        self.string_entry.grid(row=9, column=0, padx=10, pady=5, columnspan=8)

    def limpar(self):
        self.sequencias = [];
        self.escalas = [];

    def adicionar_tecla(self, nota):
        self.tecla_atual += f"{nota}"

    def adicionar_tecla_pausa(self):
        self.tecla_atual += f"P"

    def enviar(self):
        try:
            # Arduino
            if self.string_entry.get() != "":
                sequencias_string = self.string_entry.get()
            else:
                sequencias_string = "|".join(self.sequencias)

            self.arduino.write(sequencias_string.encode())

            # Teste arduino
            print("Data sent to Arduino:", sequencias_string)

            # UR
            # Create an instance of ModbusServer
            server = ModbusServer(SERVER_ADDRESS, SERVER_PORT, no_block=True)
            server.start()
            print('Server is online')

            for s in self.sequencias:
                # Using regular expressions to extract values
                tempo = int(s[s.index("T")+1:s.index("Z")])
                escala = int(s[-1])
                print(f"Time: {tempo}, Scale: {escala}")
                server.data_bank.set_input_registers(180, [escala])
                    
                # Introduce a delay based on the time value
                sleep(tempo/1000)

            print("fim")

        except Exception as e:
            print(str(e))

    def armazenar_sequencia(self):
        sequencia = self.tecla_atual.strip()
        tempo = self.tempo_entry.get()
        escala = self.escala_entry.get()  # Captura o valor da entrada da escala
        if sequencia and tempo and escala:
            sequencia_completa = f"S{sequencia}T{tempo}Z{escala}"  # Inclui a escala na sequência
            escala_completa = f"T{tempo}Z{escala}"
            self.sequencias.append(sequencia_completa)
            self.escalas.append(escala_completa)
            self.tecla_atual = ""
            #self.tempo_entry.delete(0, "end")
            #self.escala_entry.delete(0, "end")  # Limpa o campo da escala
            print("Sequência armazenada:", sequencia_completa)
            print("Todas as sequências:", self.sequencias)

class HomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Home")

        # Configure o estilo das abas
        aba_style = ttk.Style()
        aba_style.configure("TNotebook.Tab", background="lightblue", foreground="black", font=("Helvetica", 12), relief="raised", borderwidth=2, padx=10, pady=5)

        self.criar_interface()

    def criar_interface(self):
        # Botão "Criar código"
        criar_codigo_botao = tk.Button(self.root, text="Criar código", command=self.ir_para_piano, font=("Arial", 12, "bold"), bg="green", fg="white", borderwidth=2, relief="raised")
        criar_codigo_botao.grid(row=0, column=0, padx=10, pady=10)

        # Botão "Carregar música"
        carregar_musica_botao = tk.Button(self.root, text="Carregar música", command=self.ir_para_carregar_musica, font=("Arial", 12, "bold"), bg="blue", fg="white", borderwidth=2, relief="raised")
        carregar_musica_botao.grid(row=1, column=0, padx=10, pady=10)

    def ir_para_piano(self):
        root = tk.Toplevel(self.root)
        app = PianoApp(root)

    def ir_para_carregar_musica(self):
        root = tk.Toplevel(self.root)
        app = CarregarMusicaApp(root)

class CarregarMusicaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Carregar Música")

        self.arquivo_midi = None
        self.string_midi = None

        self.criar_interface()

    def criar_interface(self):
        # Botão para carregar arquivo MIDI
        carregar_arquivo_botao = tk.Button(self.root, text="Carregar Arquivo MIDI", command=self.carregar_arquivo_midi)
        carregar_arquivo_botao.grid(row=0, column=0, padx=10, pady=10)

        # Botão para converter arquivo MIDI em string
        converter_string_botao = tk.Button(self.root, text="Converter em String", command=self.converter_em_string)
        converter_string_botao.grid(row=1, column=0, padx=10, pady=10)

        # Rótulo para exibir a string MIDI
        self.string_midi_label = tk.Label(self.root, text="")
        self.string_midi_label.grid(row=2, column=0, padx=10, pady=10)

    def carregar_arquivo_midi(self):
        # Abre uma janela de diálogo para selecionar o arquivo MIDI
        arquivo_midi = filedialog.askopenfilename(filetypes=[("Arquivos MIDI", "*.mid")])

        if arquivo_midi:
            self.arquivo_midi = arquivo_midi

    def converter_em_string(self):
        if self.arquivo_midi:
            try:
                with open(self.arquivo_midi, 'rb') as arquivo:
                    mensagens = mido.MidiFile(self.arquivo_midi)
                    midi_string = "\n".join(str(mensagem) for mensagem in mensagens)

                    self.string_midi = midi_string
                    self.string_midi_label.config(text="String MIDI:\n" + midi_string)
            except Exception as e:
                self.string_midi_label.config(text="Erro ao carregar o arquivo MIDI.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HomeApp(root)
    root.mainloop()