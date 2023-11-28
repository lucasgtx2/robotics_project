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
        self.i = 0
        self.musica = ""

        # Carregando a imagem
        self.imagem = tk.PhotoImage(file="img/playbut.png")
        self.imagem = self.imagem.subsample(16, 16)

        # Inicialização da comunicação serial com Arduino
        self.arduino = serial.Serial(port='COM7', baudrate=9600, timeout=1)

        self.server = ModbusServer(SERVER_ADDRESS, SERVER_PORT, no_block=True)
        self.server.start()
        print('Server is online')

        self.criar_interface()

    def criar_interface(self):
        # Título
        title = tk.Label(self.root, text="Crie uma música no teclado virtual", font=("Consolas", 14))
        title.grid(row=0, column=0, columnspan=8, pady=5)

        # Criação de botões brancos (teclas)
        notas_brancas = ["C", "D", "E", "F", "G", "A", "B", "NADA"]  # Adicionei "NADA"
        for i, nota in enumerate(notas_brancas):
            if nota == "NADA":
                tecla = tk.Button(self.root, text=nota, command=lambda nota=nota: self.adicionar_tecla_pausa(),
                                width=4, height=10, font=("Consolas", 10, "bold"))
            else:
                tecla = tk.Button(self.root, text="", command=lambda nota=nota: self.adicionar_tecla(nota),
                                width=4, height=10, bg="white")
            tecla.grid(row=1, column=i, padx=5, pady=5)
            self.teclas.append(tecla)

        # Criação de botões pretos (sustenidos)
        notas_pretas = ["J", "K", "L", "M", "N"]
        i=0
        for nota in notas_pretas:
            tecla = tk.Button(self.root, text="", command=lambda nota=nota: self.adicionar_tecla(nota),
                            bg="black", fg="white", width=2, height=6)
            if nota in ["J", "K"]:
                tecla.grid(row=1, column=i + 1, padx=5, pady=5)
                i += 1
            else:
                i += 1
                tecla.grid(row=1, column=i + 1, padx=5, pady=5)
            self.teclas.append(tecla)

        # Vazio
        vazio = tk.Label(self.root, text="")
        vazio.grid(row=2, column=0, columnspan=8, pady=5)

        # Títulos "Digite o tempo" e "Digite a Escala (0:5)"
        escala_label = tk.Label(self.root, text="Escala (0:4)", font=("Consolas", 10))
        escala_label.grid(row=3, column=0, columnspan=4, pady=5)
        tempo_label = tk.Label(self.root, text="Tempo (ms)", font=("Consolas", 10))
        tempo_label.grid(row=3, column=4, columnspan=4, pady=5)

        # Campos de entrada para o tempo e a escala
        self.escala_entry = tk.Entry(self.root)
        self.escala_entry.grid(row=4, column=0, columnspan=4, pady=5)
        self.tempo_entry = tk.Entry(self.root)
        self.tempo_entry.grid(row=4, column=4, columnspan=4, pady=5)

        # Botão "Confirmar"
        confirmar_botao = tk.Button(self.root, text="Confirmar", command=self.armazenar_sequencia, font=("Consolas", 10))
        confirmar_botao.grid(row=5, column=2, columnspan=4, pady=8)

        # Criar um Label para exibir a imagem como botão
        play_button = tk.Label(self.root, image=self.imagem, bd=0, cursor="hand2")
        play_button.bind("<Button-1>", self.enviar)
        play_button.grid(row=6, column=2, columnspan=4, pady=10)

        # Título "Inserir música"
        inserir_musica_label = tk.Label(self.root, text="Ou digite uma música completa", font=("Consolas", 12))
        inserir_musica_label.grid(row=7, column=0, columnspan=8, pady=5)

        # Campo de entrada para a música completa
        self.string_entry = tk.Entry(self.root)
        self.string_entry.grid(row=8, column=0, columnspan=8, pady=5)

        # Botão "Limpar Sequência"
        limpar_botao = tk.Button(self.root, text="Limpar Sequência", command=self.limpar, font=("Consolas", 10))
        limpar_botao.grid(row=9, column=2, columnspan=4, pady=10)

        # Vazio
        vazio2 = tk.Label(self.root, text="")
        vazio2.grid(row=10, column=0, columnspan=8, pady=10)

        # Título de músicas prontas
        musicas_prontas = tk.Label(self.root, text="Ou selecione uma música pronta", font=("Consolas", 12))
        musicas_prontas.grid(row=11, column=0, columnspan=8, pady=10)

        # Músicas 1, 2 e 3
        musica1 = tk.Label(self.root, text="Música 1", font=("Consolas", 10), bd=0, cursor="hand2")
        musica1.bind("<Button-1>", self.musica1)
        musica1.grid(row=12, column=0, columnspan=4, pady=10)

        musica2 = tk.Label(self.root, text="Música 2", font=("Consolas", 10), bd=0, cursor="hand2")
        musica2.bind("<Button-1>", self.musica2)
        musica2.grid(row=12, column=2, columnspan=4, pady=10)

        musica3 = tk.Label(self.root, text="Música 3", font=("Consolas", 10), bd=0, cursor="hand2")
        musica3.bind("<Button-1>", self.musica3)
        musica3.grid(row=12, column=4, columnspan=4, pady=10)

        self.root.mainloop()


    def musica1(self, event):
        self.musica = ""

    def musica2(self, event):
        self.musica = ""

    def musica3(self, event):
        self.musica = ""

    def limpar(self):
        self.sequencias = []
        self.escalas = []
        self.string_entry.delete('0', 'end')

    def adicionar_tecla(self, nota):
        self.tecla_atual += f"{nota}"

    def adicionar_tecla_pausa(self):
        self.tecla_atual += f"P"

    def enviar(self,event):
        try:
            # UR
            if self.string_entry.get() != "":
                sequencias_list = self.string_entry.get().split("|")
                sequencias_string = self.string_entry.get()
            else:
                sequencias_list = self.sequencias
                sequencias_string = "|".join(self.sequencias)

            # Referenciamento na escala do primeiro acorde
            self.server.data_bank.set_input_registers(181, [1])
            self.server.data_bank.set_input_registers(180, [int((sequencias_list[0])[-1])])

            print("Start UR5")
            sleep(3)

            self.arduino.write(sequencias_string.encode())
            print("Data sent to Arduino:", sequencias_string)

            sleep(1) # sincronização da comunicação
            for s in sequencias_list:
                tempo = int(s[s.index("T")+1:s.index("Z")])
                escala = int(s[-1])
                self.server.data_bank.set_input_registers(180, [escala])
                print(f"Time: {tempo}, Scale: {escala}")
                
                # Introduce a delay based on the time value
                sleep(tempo/1000)

            print("fim")
            self.server.data_bank.set_input_registers(181, [0])

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
            print("Sequência armazenada:", sequencia_completa)
            print("Todas as sequências:", self.sequencias)

class HomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Home")

        # Configure o estilo das abas
        aba_style = ttk.Style()
        aba_style.configure("TNotebook.Tab", background="lightblue", foreground="black", font=("Consolas", 12), relief="raised", borderwidth=2, padx=10, pady=5)

        self.criar_interface()

    def criar_interface(self):
        # Título da aba
        titulo_label = tk.Label(self.root, text="Olá, eu sou o PianoBot!", font=("Consolas", 25, "bold"))
        titulo_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Descrição da aba
        descricao_label = tk.Label(self.root, text="Clique no botão e me ensine a tocar uma música", font=("Consolas", 16))
        descricao_label.grid(row=1, column=0, padx=10, pady=5, columnspan=2)

        # Botão "Criar código"
        criar_codigo_botao = tk.Button(self.root, text="Criar música", command=self.ir_para_piano, font=("Consolas", 14, "bold"), bg="#BEE1EA", fg="grey")
        criar_codigo_botao.grid(row=2, column=0, padx=300, pady=30)
        criar_codigo_botao.config(width=20, height=2)

    def ir_para_piano(self):
        root = tk.Toplevel(self.root)
        app = PianoApp(root)

if __name__ == "__main__":
    root = tk.Tk()
    app = HomeApp(root)
    root.mainloop()