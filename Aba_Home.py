import tkinter as tk
from tkinter import filedialog
import mido

class PianoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Piano")

        self.teclas = []
        self.tecla_atual = ""
        self.sequencias = []

        self.criar_interface()

    def criar_interface(self):
        # Criação de botões brancos (teclas)
        notas_brancas = ["C", "D", "E", "F", "G", "A", "B"]
        for nota in notas_brancas:
            tecla = tk.Button(self.root, text=nota, command=lambda nota=nota: self.adicionar_tecla(nota), width=4, height=10)
            tecla.grid(row=0, column=notas_brancas.index(nota), padx=5, pady=5)
            self.teclas.append(tecla)

        # Criação de botões pretos (sustenidos)
        notas_pretas = ["C#", "D#", "F#", "G#", "A#"]
        for nota in notas_pretas:
            tecla = tk.Button(self.root, text=nota, command=lambda nota=nota: self.adicionar_tecla(nota), bg="black", fg="white", width=2, height=6)
            tecla.grid(row=0, column=notas_brancas.index(nota[0]) + 1, padx=5, pady=5)
            self.teclas.append(tecla)

        # Título "Digite o tempo"
        tempo_label = tk.Label(self.root, text="Digite o tempo")
        tempo_label.grid(row=1, column=0, padx=10, pady=5, columnspan=8)

        # Campo de entrada para o tempo
        self.tempo_entry = tk.Entry(self.root)
        self.tempo_entry.grid(row=2, column=0, padx=10, pady=5, columnspan=8)

        # Botão para confirmar a sequência
        confirmar_botao = tk.Button(self.root, text="Confirmar", command=self.armazenar_sequencia)
        confirmar_botao.grid(row=3, column=0, padx=10, pady=10, columnspan=8)

    def adicionar_tecla(self, nota):
        self.tecla_atual += f"{nota} "

    def armazenar_sequencia(self):
        sequencia = self.tecla_atual.strip()
        tempo = self.tempo_entry.get()
        if sequencia and tempo:
            sequencia_com_tempo = f"{sequencia} | Tempo: {tempo}"
            self.sequencias.append(sequencia_com_tempo)
            self.tecla_atual = ""
            self.tempo_entry.delete(0, "end")
            print("Sequência armazenada:", sequencia_com_tempo)
            print("Todas as sequências:", self.sequencias)

class HomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Home")

        self.criar_interface()

    def criar_interface(self):
        # Botão "Criar código"
        criar_codigo_botao = tk.Button(self.root, text="Criar código", command=self.ir_para_piano)
        criar_codigo_botao.grid(row=0, column=0, padx=10, pady=10)

        # Botão "Carregar música"
        carregar_musica_botao = tk.Button(self.root, text="Carregar música", command=self.ir_para_carregar_musica)
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
