import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime


DB_FILE = "bug_bounty_tasks.json"


DEFAULT_TASKS = [
    {"title": "Identify real IP address", "done": False, "priority": "High"},
    {"title": "Check for CDN/WAF", "done": False, "priority": "Medium"},
    {"title": "Enumerate open ports", "done": False, "priority": "High"},
    {"title": "Enumerate port services", "done": False, "priority": "High"},
    {"title": "Enumerate web services", "done": False, "priority": "High"},
    {"title": "Search for public exploits", "done": False, "priority": "Medium"},
    {"title": "Run default template fuzzing", "done": False, "priority": "Medium"},
    {"title": "Run service-based fuzzing", "done": False, "priority": "Medium"},
    {"title": "Run Nuclei templates", "done": False, "priority": "High"},
    {"title": "Run ZAP baseline scan", "done": False, "priority": "Medium"},
    {"title": "Check for login page", "done": False, "priority": "High"},
    {"title": "Check for registration page", "done": False, "priority": "Medium"},
    {"title": "Check password reset flow", "done": False, "priority": "High"},
    {"title": "Check for file upload features", "done": False, "priority": "High"},
    {"title": "Check for internal panels", "done": False, "priority": "High"},
    {"title": "Check for /admin area", "done": False, "priority": "High"},
    {"title": "Check for API directories", "done": False, "priority": "High"},
]


def load_database():
    if not os.path.exists(DB_FILE):
        return {}

    try:
        with open(DB_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        messagebox.showerror("Error", "Database file is corrupted.")
        return {}


def save_database(data):
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def create_host_profile(host):
    return {
        "host": host,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "notes": "",
        "tasks": DEFAULT_TASKS.copy(),
    }


class BugBountyTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bug Bounty Recon Checklist")
        self.root.geometry("850x600")

        self.data = load_database()
        self.current_host = None
        self.task_vars = []

        self.setup_layout()
        self.refresh_host_list()

    def setup_layout(self):
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(
            self.left_frame,
            text="Targets",
            font=("Arial", 13, "bold")
        ).pack(anchor="w")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh_host_list())

        self.search_entry = ttk.Entry(
            self.left_frame,
            textvariable=self.search_var
        )
        self.search_entry.pack(fill=tk.X, pady=(5, 5))
        self.search_entry.insert(0, "")

        self.host_listbox = tk.Listbox(self.left_frame, width=32, height=22)
        self.host_listbox.pack(fill=tk.Y, expand=True)
        self.host_listbox.bind("<<ListboxSelect>>", self.on_host_selected)

        ttk.Button(
            self.left_frame,
            text="Add Target",
            command=self.add_host
        ).pack(fill=tk.X, pady=(10, 3))

        ttk.Button(
            self.left_frame,
            text="Remove Target",
            command=self.remove_host
        ).pack(fill=tk.X, pady=3)

        ttk.Button(
            self.left_frame,
            text="Reset Target Tasks",
            command=self.reset_host_tasks
        ).pack(fill=tk.X, pady=3)

        self.host_title = ttk.Label(
            self.right_frame,
            text="Select a target",
            font=("Arial", 15, "bold")
        )
        self.host_title.pack(anchor="w")

        self.progress_label = ttk.Label(
            self.right_frame,
            text="Progress: 0%"
        )
        self.progress_label.pack(anchor="w", pady=(5, 2))

        self.progress_bar = ttk.Progressbar(
            self.right_frame,
            length=400,
            mode="determinate"
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))

        self.task_container = ttk.LabelFrame(
            self.right_frame,
            text="Recon Tasks",
            padding=10
        )
        self.task_container.pack(fill=tk.BOTH, expand=True)

        self.task_canvas = tk.Canvas(self.task_container)
        self.task_scrollbar = ttk.Scrollbar(
            self.task_container,
            orient=tk.VERTICAL,
            command=self.task_canvas.yview
        )

        self.task_list_frame = ttk.Frame(self.task_canvas)

        self.task_list_frame.bind(
            "<Configure>",
            lambda event: self.task_canvas.configure(
                scrollregion=self.task_canvas.bbox("all")
            )
        )

        self.task_canvas.create_window(
            (0, 0),
            window=self.task_list_frame,
            anchor="nw"
        )

        self.task_canvas.configure(yscrollcommand=self.task_scrollbar.set)

        self.task_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.task_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_buttons_frame = ttk.Frame(self.right_frame)
        self.task_buttons_frame.pack(fill=tk.X, pady=8)

        ttk.Button(
            self.task_buttons_frame,
            text="Add Task",
            command=self.add_task
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            self.task_buttons_frame,
            text="Remove Completed Tasks",
            command=self.remove_completed_tasks
        ).pack(side=tk.LEFT, padx=5)

        self.notes_frame = ttk.LabelFrame(
            self.right_frame,
            text="Target Notes",
            padding=10
        )
        self.notes_frame.pack(fill=tk.BOTH, pady=(5, 0))

        self.notes_text = tk.Text(self.notes_frame, height=5)
        self.notes_text.pack(fill=tk.BOTH, expand=True)

        ttk.Button(
            self.notes_frame,
            text="Save Notes",
            command=self.save_notes
        ).pack(anchor="e", pady=(5, 0))

    def refresh_host_list(self):
        search = self.search_var.get().lower().strip()

        self.host_listbox.delete(0, tk.END)

        for host in sorted(self.data.keys()):
            if search and search not in host.lower():
                continue

            progress = self.calculate_progress(host)
            self.host_listbox.insert(tk.END, f"{host}  [{progress}%]")

    def get_selected_host_from_listbox(self):
        selection = self.host_listbox.curselection()

        if not selection:
            return None

        item = self.host_listbox.get(selection[0])
        return item.split("  [")[0]

    def add_host(self):
        host = simpledialog.askstring(
            "Add Target",
            "Enter target host or domain:"
        )

        if not host:
            return

        host = host.strip().lower()

        if host in self.data:
            messagebox.showerror("Error", "This target already exists.")
            return

        self.data[host] = create_host_profile(host)
        self.save_and_refresh()

    def remove_host(self):
        host = self.get_selected_host_from_listbox()

        if not host:
            messagebox.showwarning("Warning", "Select a target first.")
            return

        confirm = messagebox.askyesno(
            "Confirm",
            f"Remove target '{host}'?"
        )

        if not confirm:
            return

        del self.data[host]
        self.current_host = None
        self.clear_task_list()
        self.host_title.config(text="Select a target")
        self.update_progress()
        self.save_and_refresh()

    def reset_host_tasks(self):
        host = self.get_selected_host_from_listbox()

        if not host:
            messagebox.showwarning("Warning", "Select a target first.")
            return

        confirm = messagebox.askyesno(
            "Confirm",
            f"Reset all tasks for '{host}'?"
        )

        if not confirm:
            return

        self.data[host]["tasks"] = DEFAULT_TASKS.copy()
        self.data[host]["updated_at"] = datetime.now().isoformat(timespec="seconds")
        self.save_and_refresh()

        if self.current_host == host:
            self.load_tasks(host)

    def on_host_selected(self, event=None):
        host = self.get_selected_host_from_listbox()

        if not host:
            return

        self.current_host = host
        self.host_title.config(text=host)
        self.load_tasks(host)
        self.load_notes(host)
        self.update_progress()

    def clear_task_list(self):
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        self.task_vars.clear()

    def load_tasks(self, host):
        self.clear_task_list()

        tasks = self.data[host].get("tasks", [])

        for index, task in enumerate(tasks):
            row = ttk.Frame(self.task_list_frame)
            row.pack(fill=tk.X, pady=2)

            var = tk.BooleanVar(value=task.get("done", False))

            checkbox = ttk.Checkbutton(
                row,
                text=task.get("title", ""),
                variable=var,
                command=lambda i=index, v=var: self.update_task_status(i, v.get())
            )
            checkbox.pack(side=tk.LEFT, fill=tk.X, expand=True)

            priority = task.get("priority", "Medium")

            priority_label = ttk.Label(
                row,
                text=priority,
                width=10
            )
            priority_label.pack(side=tk.LEFT, padx=5)

            edit_button = ttk.Button(
                row,
                text="Edit",
                width=8,
                command=lambda i=index: self.edit_task(i)
            )
            edit_button.pack(side=tk.LEFT, padx=2)

            delete_button = ttk.Button(
                row,
                text="Delete",
                width=8,
                command=lambda i=index: self.delete_task(i)
            )
            delete_button.pack(side=tk.LEFT, padx=2)

            self.task_vars.append(var)

    def update_task_status(self, index, done):
        if not self.current_host:
            return

        self.data[self.current_host]["tasks"][index]["done"] = done
        self.data[self.current_host]["updated_at"] = datetime.now().isoformat(timespec="seconds")

        self.save_and_refresh()
        self.update_progress()

    def add_task(self):
        if not self.current_host:
            messagebox.showwarning("Warning", "Select a target first.")
            return

        title = simpledialog.askstring(
            "Add Task",
            "Task name:"
        )

        if not title:
            return

        priority = simpledialog.askstring(
            "Task Priority",
            "Priority: Low, Medium, High",
            initialvalue="Medium"
        )

        if priority not in {"Low", "Medium", "High"}:
            priority = "Medium"

        self.data[self.current_host]["tasks"].append({
            "title": title.strip(),
            "done": False,
            "priority": priority,
        })

        self.data[self.current_host]["updated_at"] = datetime.now().isoformat(timespec="seconds")

        self.save_and_refresh()
        self.load_tasks(self.current_host)
        self.update_progress()

    def edit_task(self, index):
        if not self.current_host:
            return

        task = self.data[self.current_host]["tasks"][index]

        new_title = simpledialog.askstring(
            "Edit Task",
            "Task name:",
            initialvalue=task.get("title", "")
        )

        if not new_title:
            return

        new_priority = simpledialog.askstring(
            "Edit Priority",
            "Priority: Low, Medium, High",
            initialvalue=task.get("priority", "Medium")
        )

        if new_priority not in {"Low", "Medium", "High"}:
            new_priority = "Medium"

        task["title"] = new_title.strip()
        task["priority"] = new_priority
        self.data[self.current_host]["updated_at"] = datetime.now().isoformat(timespec="seconds")

        self.save_and_refresh()
        self.load_tasks(self.current_host)

    def delete_task(self, index):
        if not self.current_host:
            return

        task_title = self.data[self.current_host]["tasks"][index]["title"]

        confirm = messagebox.askyesno(
            "Confirm",
            f"Delete task '{task_title}'?"
        )

        if not confirm:
            return

        del self.data[self.current_host]["tasks"][index]
        self.data[self.current_host]["updated_at"] = datetime.now().isoformat(timespec="seconds")

        self.save_and_refresh()
        self.load_tasks(self.current_host)
        self.update_progress()

    def remove_completed_tasks(self):
        if not self.current_host:
            messagebox.showwarning("Warning", "Select a target first.")
            return

        self.data[self.current_host]["tasks"] = [
            task for task in self.data[self.current_host]["tasks"]
            if not task.get("done", False)
        ]

        self.data[self.current_host]["updated_at"] = datetime.now().isoformat(timespec="seconds")

        self.save_and_refresh()
        self.load_tasks(self.current_host)
        self.update_progress()

    def load_notes(self, host):
        self.notes_text.delete("1.0", tk.END)
        self.notes_text.insert(
            tk.END,
            self.data[host].get("notes", "")
        )

    def save_notes(self):
        if not self.current_host:
            messagebox.showwarning("Warning", "Select a target first.")
            return

        notes = self.notes_text.get("1.0", tk.END).strip()

        self.data[self.current_host]["notes"] = notes
        self.data[self.current_host]["updated_at"] = datetime.now().isoformat(timespec="seconds")

        self.save_and_refresh()
        messagebox.showinfo("Saved", "Notes saved successfully.")

    def calculate_progress(self, host):
        tasks = self.data[host].get("tasks", [])

        if not tasks:
            return 0

        completed = sum(1 for task in tasks if task.get("done", False))
        return int((completed / len(tasks)) * 100)

    def update_progress(self):
        if not self.current_host:
            self.progress_label.config(text="Progress: 0%")
            self.progress_bar["value"] = 0
            return

        progress = self.calculate_progress(self.current_host)

        self.progress_label.config(text=f"Progress: {progress}%")
        self.progress_bar["value"] = progress

    def save_and_refresh(self):
        save_database(self.data)
        self.refresh_host_list()


if __name__ == "__main__":
    root = tk.Tk()
    app = BugBountyTodoApp(root)
    root.mainloop()
