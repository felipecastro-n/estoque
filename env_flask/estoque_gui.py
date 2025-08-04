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

        top_frame = tk.Frame(self.frame_lista)
        top_frame.pack(fill="x")
        tk.Button(top_frame, text="Voltar", command=self.build_menu).pack(side="left")
        tk.Label(top_frame, text="Buscar peça por nome/código OEM:").pack(side="left", padx=5)
        self.entry_busca = tk.Entry(top_frame)
        self.entry_busca.pack(side="left")
        tk.Button(top_frame, text="Buscar", command=self.buscar_peca).pack(side="left", padx=5)

        # Campo para buscar por UID RFID
        tk.Label(top_frame, text="ou UID RFID:").pack(side="left", padx=5)
        self.entry_rfid = tk.Entry(top_frame, width=20)
        self.entry_rfid.pack(side="left")
        tk.Button(top_frame, text="Buscar RFID", command=self.buscar_por_rfid).pack(side="left", padx=5)

        columns = ("id", "nome", "codigo_oem", "descricao", "localizacao", "quantidade", "preco_custo", "preco_venda", "modelo_carro", "ano_carro", "rfid_uid")
        self.tree = ttk.Treeview(self.frame_lista, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # Botão para associar RFID à peça selecionada
        btn_rfid = tk.Button(self.frame_lista, text="Associar RFID à peça selecionada", command=self.associar_rfid)
        btn_rfid.pack(pady=5)

        self.carregar_pecas()

    def carregar_pecas(self, filtro=None):
        # Limpa a tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            resp = requests.get(f"{API_URL}/pecas", headers=headers)
            if resp.status_code == 200:
                pecas = resp.json()
                if filtro:
                    filtro = filtro.lower()
                    pecas = [p for p in pecas if filtro in p["nome"].lower() or filtro in p["codigo_oem"].lower()]
                for peca in pecas:
                    self.tree.insert("", "end", values=(
                        peca["id"], peca["nome"], peca["codigo_oem"], peca["descricao"], peca["localizacao"],
                        peca["quantidade"], peca["preco_custo"], peca["preco_venda"], peca["modelo_carro"], peca["ano_carro"],
                        peca.get("rfid_uid", "")
                    ))
            else:
                messagebox.showerror("Erro", "Não foi possível listar as peças.\nFaça login novamente.")
                self.logout()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar à API: {e}")
            self.logout()
    def buscar_por_rfid(self):
        uid = self.entry_rfid.get().strip()
        if not uid:
            messagebox.showwarning("Aviso", "Digite o UID RFID para buscar.")
            return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            resp = requests.get(f"{API_URL}/pecas/rfid/{uid}", headers=headers)
            for item in self.tree.get_children():
                self.tree.delete(item)
            if resp.status_code == 200:
                peca = resp.json()
                self.tree.insert("", "end", values=(
                    peca["id"], peca["nome"], peca["codigo_oem"], peca["descricao"], peca["localizacao"],
                    peca["quantidade"], peca["preco_custo"], peca["preco_venda"], peca["modelo_carro"], peca["ano_carro"],
                    peca.get("rfid_uid", "")
                ))
            else:
                messagebox.showinfo("Info", "Peça não encontrada para este UID.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar à API: {e}")

    def associar_rfid(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma peça na lista.")
            return
        peca_id = self.tree.item(selected[0])["values"][0]
        uid = tk.simpledialog.askstring("Associar RFID", "Digite o UID RFID a associar à peça:")
        if not uid:
            return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            resp = requests.patch(f"{API_URL}/pecas/{peca_id}/rfid", json={"rfid_uid": uid}, headers=headers)
            if resp.status_code == 200:
                messagebox.showinfo("Sucesso", "RFID associado à peça!")
                self.carregar_pecas()
            else:
                erro = resp.json().get("error", "Erro ao associar RFID.")
                messagebox.showerror("Erro", erro)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar à API: {e}")

    def buscar_peca(self):
        termo = self.entry_busca.get().strip()
        self.carregar_pecas(filtro=termo)

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

