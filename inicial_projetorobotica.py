import tkinter as tk

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
        tempo_label.grid(row=1, column=0, padx=5, pady=5, columnspan=8)

        # Campo de entrada para o tempo
        self.tempo_entry = tk.Entry(self.root)
        self.tempo_entry.grid(row=2, column=0, padx=5, pady=5, columnspan=8)

        # Botão para confirmar a sequência
        confirmar_botao = tk.Button(self.root, text="Confirmar", command=self.armazenar_sequencia)
        confirmar_botao.grid(row=3, column=0, padx=5, pady=5, columnspan=8)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = PianoApp(root)
    root.mainloop()
