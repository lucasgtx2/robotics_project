    tecla = tk.Button(self.root, text="", command=lambda nota=nota: self.adicionar_tecla(nota),
                            bg="black", fg="white", width=2, height=6)
            if nota in ["J", "K"]:
                tecla.grid(row=1, column=i + 1, padx=5, pady=5)
                i += 1
            else:
                i += 1
                tecla.grid(row=1, column=i + 1, padx=5, pady=5)
            self.teclas.append(tecla)