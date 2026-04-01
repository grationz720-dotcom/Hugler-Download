import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Для работы с картинками
import requests
from io import BytesIO # Чтобы скачивать картинку в память
import json
import os
import sys
import subprocess
import webbrowser

CURRENT_VERSION = "1.0.0"
# Замени на прямую ссылку на твой логотип (RAW)
LOGO_URL = "https://githubusercontent.com"
CONFIG_URL = "https://githubusercontent.com"

class HuglerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Hugler Download v{CURRENT_VERSION}")
        self.root.geometry("450x650")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)
        
        self.data = self.load_config()
        self.create_gui()

    def load_config(self):
        try:
            r = requests.get(CONFIG_URL, timeout=3)
            return r.json()
        except:
            if os.path.exists("huglerconfig.json"):
                with open("huglerconfig.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            return {"project_name": "Offline Mode", "version": "0.0.0", "libraries": [], "github_link": "#", "socials": "#"}

    def create_gui(self):
        # ЗАГРУЗКА ЛОГОТИПА ИЗ ИНТЕРНЕТА
        try:
            response = requests.get(LOGO_URL, timeout=5)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((200, 200), Image.Resampling.LANCZOS) # Подгоняем размер
            self.logo_img = ImageTk.PhotoImage(img)
            
            tk.Label(self.root, image=self.logo_img, bg="#121212").pack(pady=20)
        except:
            # Если инета нет, просто пишем текст
            tk.Label(self.root, text="[ HUGLER ]", font=("Arial", 24, "bold"), fg="#00ffcc", bg="#121212").pack(pady=40)

        tk.Label(self.root, text=f"PROJECT: {self.data['project_name']}", font=("Arial", 16, "bold"), fg="white", bg="#121212").pack()
        tk.Label(self.root, text=f"Version: {self.data['version']}", fg="#888888", bg="#121212").pack(pady=5)

        tk.Button(self.root, text="OPEN GITHUB", command=lambda: webbrowser.open(self.data['github_link']), 
                  bg="#333333", fg="white", width=25, bd=0, height=2).pack(pady=10)
        
        tk.Button(self.root, text="SOCIAL NETWORKS", command=lambda: webbrowser.open(self.data['socials']), 
                  bg="#333333", fg="white", width=25, bd=0, height=2).pack(pady=5)

        self.status = tk.Label(self.root, text="SYSTEM READY", fg="#00ffcc", bg="#121212", font=("Arial", 11, "bold"))
        self.status.pack(pady=30)

        self.btn = tk.Button(self.root, text="START INSTALLATION", command=self.start_sync, 
                             bg="#00ffcc", fg="black", font=("Arial", 12, "bold"), width=25, height=2, bd=0)
        self.btn.pack()

    def start_sync(self):
        libs = self.data.get("libraries", [])
        self.btn.config(state="disabled", text="WORKING...")
        
        for lib in libs:
            lib_name = lib.strip()
            if lib_name:
                self.status.config(text=f"DOWNLOADING: {lib_name}", fg="#ffcc00")
                self.root.update()
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", lib_name])
                except:
                    print(f"Error with {lib_name}")
        
        self.status.config(text="ALL LIBRARIES SYNCED", fg="#00ffcc")
        self.btn.config(state="normal", text="COMPLETE")
        messagebox.showinfo("Hugler", "Project synchronization complete!")

if __name__ == "__main__":
    root = tk.Tk()
    app = HuglerApp(root)
    root.mainloop()
