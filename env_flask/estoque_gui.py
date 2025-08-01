# Salve como estoque_gui.py e execute com o ambiente ativado

import tkinter as tk
from tkinter import messagebox, ttk
import requests

API_URL = "http://localhost:5000"

class EstoqueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Estoque Toyota Newland")
        self.token = None

        self.frame_login = tk.Frame(root)
        self.frame_menu = tk.Frame(root)
        self.frame_cadastro = tk.Frame(root)
        self.frame_lista = tk.Frame(root)

        self.build_login()

    def build_login(self):
        self.clear_frames()
        self.frame_login.pack(padx=20, pady=20)

        tk.Label(self.frame_login, text="Usuário:").grid(row=0, column=0, sticky="e")
        self.entry_user = tk.Entry(self.frame_login)
        self.entry_user.grid(row=0, column=1)

        tk.Label(self.frame_login, text="Senha:").grid(row=1, column=0, sticky="e")
        self.entry_pass = tk.Entry(self.frame_login, show="*")
        self.entry_pass.grid(row=1, column=1)

        tk.Button(self.frame_login, text="Entrar", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)

    def build_menu(self):
        self.clear_frames()
        self.frame_menu.pack(padx=20, pady=20)

        tk.Label(self.frame_menu, text="Bem-vindo ao Estoque Toyota Newland!", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.frame_menu, text="Cadastrar Peça", width=20, command=self.build_cadastro).pack(pady=5)
        tk.Button(self.frame_menu, text="Listar Peças", width=20, command=self.build_lista).pack(pady=5)
        tk.Button(self.frame_menu, text="Sair", width=20, command=self.logout).pack(pady=5)

    def build_cadastro(self):
        self.clear_frames()
        self.frame_cadastro.pack(padx=20, pady=20)

        labels = [
            "Nome", "Código OEM", "Descrição", "Localização", "Quantidade",
            "Preço Custo", "Preço Venda", "Modelo Carro", "Ano Carro"
        ]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(self.frame_cadastro, text=label + ":").grid(row=i, column=0, sticky="e")
            entry = tk.Entry(self.frame_cadastro)
            entry.grid(row=i, column=1)
            self.entries[label] = entry

        tk.Button(self.frame_cadastro, text="Cadastrar", command=self.cadastrar_peca).grid(row=len(labels), column=0, columnspan=2, pady=10)
        tk.Button(self.frame_cadastro, text="Voltar", command=self.build_menu).grid(row=len(labels)+1, column=0, columnspan=2)

    def build_lista(self):
        self.clear_frames()
        self.frame_lista.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Button(self.frame_lista, text="Voltar", command=self.build_menu).pack(anchor="w")

        columns = ("id", "nome", "codigo_oem", "descricao", "localizacao", "quantidade", "preco_custo", "preco_venda", "modelo_carro", "ano_carro")
        tree = ttk.Treeview(self.frame_lista, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        tree.pack(fill="both", expand=True)

        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            resp = requests.get(f"{API_URL}/pecas", headers=headers)
            if resp.status_code == 200:
                for peca in resp.json():
                    tree.insert("", "end", values=(
                        peca["id"], peca["nome"], peca["codigo_oem"], peca["descricao"], peca["localizacao"],
                        peca["quantidade"], peca["preco_custo"], peca["preco_venda"], peca["modelo_carro"], peca["ano_carro"]
                    ))
            else:
                messagebox.showerror("Erro", "Não foi possível listar as peças.\nFaça login novamente.")
                self.logout()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar à API: {e}")
            self.logout()

    def login(self):
        usuario = self.entry_user.get()
        senha = self.entry_pass.get()
        try:
            resp = requests.post(f"{API_URL}/login", json={"username": usuario, "password": senha})
            if resp.status_code == 200:
                self.token = resp.json()["access_token"]
                self.build_menu()
            else:
                messagebox.showerror("Erro", "Usuário ou senha inválidos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar à API: {e}")

    def cadastrar_peca(self):
        dados = {
            "nome": self.entries["Nome"].get(),
            "codigo_oem": self.entries["Código OEM"].get(),
            "descricao": self.entries["Descrição"].get(),
            "localizacao": self.entries["Localização"].get(),
            "quantidade": int(self.entries["Quantidade"].get()),
            "preco_custo": float(self.entries["Preço Custo"].get()),
            "preco_venda": float(self.entries["Preço Venda"].get()),
            "modelo_carro": self.entries["Modelo Carro"].get(),
            "ano_carro": self.entries["Ano Carro"].get()
        }
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            resp = requests.post(f"{API_URL}/pecas", json=dados, headers=headers)
            if resp.status_code == 201:
                messagebox.showinfo("Sucesso", "Peça cadastrada com sucesso!")
                self.build_menu()
            else:
                erro = resp.json().get("error", "Erro ao cadastrar peça.")
                messagebox.showerror("Erro", erro)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar à API: {e}")

    def logout(self):
        self.token = None
        self.build_login()

    def clear_frames(self):
        for frame in [self.frame_login, self.frame_menu, self.frame_cadastro, self.frame_lista]:
            frame.pack_forget()
            for widget in frame.winfo_children():
                widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EstoqueApp(root)
    root.mainloop()

