import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

TASKS_TEMPLATE = [
    "Descobriu o IP Real?",
    "Tem CDN/WAF?",
    "Enumerar portas abertas",
    "Enumerar serviços das portas",
    "Enumerar serviços web",
    "Procurar exploits na internet",
    "Fazer fuzzing com templates padrão",
    "Fazer fuzzing com templates de servços",
    "Usar nuclei",
    "Usar ZAP",
    "Tem página de login?",
    "Tem página de registro?",
    "Tem sistema de recuperação de senha?",
    "Tem algum local de upload?",
    "Tem algum painel interno?",
    "Tem alguma área /admin?",
    "Tem algum diretório API?"
]

DB_FILE = "bounty_tasks.json"


def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as file:
            return json.load(file)
    return {}


def save_data(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)


class BugBountyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("BugBounty ToDo")
        self.data = load_data()
        self.current_host = None

        self.host_listbox = tk.Listbox(master, height=10)
        self.host_listbox.pack(fill=tk.X, padx=10, pady=5)
        self.host_listbox.bind('<<ListboxSelect>>', self.load_tasks)

        self.add_host_button = tk.Button(master, text="Adicionar Host", command=self.add_host)
        self.add_host_button.pack(pady=5)

        self.task_frame = tk.Frame(master)
        self.task_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        self.task_checkbuttons = []
        self.task_vars = []

        self.refresh_hosts()

    def refresh_hosts(self):
        self.host_listbox.delete(0, tk.END)
        for host in self.data.keys():
            self.host_listbox.insert(tk.END, host)

    def add_host(self):
        host = simpledialog.askstring("Novo Host", "Digite o nome do host (ex: example.com):")
        if host:
            if host in self.data:
                messagebox.showerror("Erro", "Host já existe.")
                return
            self.data[host] = [{"task": t, "done": False} for t in TASKS_TEMPLATE]
            save_data(self.data)
            self.refresh_hosts()

    def load_tasks(self, event):
        selection = self.host_listbox.curselection()
        if not selection:
            return

        self.current_host = self.host_listbox.get(selection[0])
        tasks = self.data[self.current_host]

        # Limpa os checkbuttons anteriores
        for cb in self.task_checkbuttons:
            cb.destroy()
        self.task_checkbuttons.clear()
        self.task_vars.clear()

        for index, task in enumerate(tasks):
            var = tk.BooleanVar(value=task["done"])
            cb = tk.Checkbutton(self.task_frame, text=task["task"], variable=var,
                                command=lambda idx=index, v=var: self.update_task(idx, v.get()))
            cb.pack(anchor="w")
            self.task_checkbuttons.append(cb)
            self.task_vars.append(var)

    def update_task(self, index, done):
        if self.current_host:
            self.data[self.current_host][index]["done"] = done
            save_data(self.data)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x500")
    app = BugBountyApp(root)
    root.mainloop()
