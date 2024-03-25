import tkinter as tk
from tkinter import ttk


class AboutForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        w = 400
        h = 150

        x = parent.winfo_x() + parent.winfo_width() // 2 - w // 2
        y = parent.winfo_y() + parent.winfo_height() // 2 - h // 2
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))

        self.title("About")
        self.resizable(False, False)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1)
        self.rowconfigure(2)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, pad=0)
        self.columnconfigure(2, weight=1)

        opts = {"padx": 5, "pady": 5, "sticky": "nswe"}

        text = tk.Text(
            self, width=40, height=3, bd=0, bg=self["bg"], wrap=tk.WORD
        )
        text.config(highlightthickness=0, borderwidth=0)
        text.insert(
            tk.INSERT,
            "Демонстрация загрузки данных в MS SQL из Excel файлов и выгрузки данных в Excel.\n",
        )
        text.insert(tk.INSERT, "email: mkhaikin@yandex.ru")

        text.configure(state="disabled")
        scroll = tk.Scrollbar(command=text.yview)
        text.config(yscrollcommand=scroll.set)
        text.grid(row=0, column=0, columnspan=3, **opts)

        text_git = tk.Text(
            self,
            height=1,
            bd=0,
            bg=self["bg"],
        )
        text_git.insert(
            tk.INSERT, "https://github.com/mkhaykin/pythonCherkizovo"
        )
        text_git.config(highlightthickness=0, borderwidth=0)
        text_git.configure(state="disabled")
        text_git.grid(row=1, column=0, columnspan=3, **opts)

        ttk.Button(self, text="Close", command=self.destroy).grid(
            row=2, column=1, **opts
        )
