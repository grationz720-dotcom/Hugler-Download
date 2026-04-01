import tkinter as tk
from tkinter import messagebox
import json

def save_config():
    # Собираем данные из полей ввода
    config = {
        "project_name": entry_name.get(),
        "version": entry_ver.get(),
        "libraries": [l.strip() for l in entry_libs.get().split(",") if l.strip()],
        "github_link": entry_git.get(),
        "socials": entry_soc.get(),
        "hugler_core": "1.0.0"
    }
    
    if not config["project_name"]:
        messagebox.showerror("Error", "Project Name is required!")
        return

    with open("huglerconfig.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    messagebox.showinfo("Hugler", "Configuration file 'huglerconfig.json' created successfully!")

# Настройка окна
root = tk.Tk()
root.title("Hugler Developer Configurator")
root.geometry("400x550")
root.configure(bg="#121212")

# Логотип (просто текст)
tk.Label(root, text="HUGLER CONFIG", font=("Arial", 16, "bold"), fg="#ffcc00", bg="#121212").pack(pady=20)

# Поля для ввода
fields = [
    ("Project Name:", "entry_name"),
    ("Version (e.g. 1.0.0):", "entry_ver"),
    ("Libraries (comma separated):", "entry_libs"),
    ("GitHub Link:", "entry_git"),
    ("Social Link:", "entry_soc")
]

entries = {}
for text, var_name in fields:
    tk.Label(root, text=text, fg="white", bg="#121212").pack(anchor="w", padx=40)
    e = tk.Entry(root, bg="#222", fg="white", insertbackground="white", width=40, bd=2)
    e.pack(pady=5)
    globals()[var_name] = e # Создаем переменные динамически

tk.Button(root, text="GENERATE JSON", command=save_config, 
          bg="#ffcc00", fg="black", font=("Arial", 10, "bold"), width=25, height=2).pack(pady=30)

root.mainloop()
