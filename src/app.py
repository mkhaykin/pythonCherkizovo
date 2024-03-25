import os
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

from tkcalendar import DateEntry

from about import AboutForm
from xlsx import export_xlsx, import_xlsx, open_xlsx


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Test sample")  # устанавливаем заголовок окна
        self.resizable(False, False)

        # w = 350
        # h = 250
        #
        # ws = self.winfo_screenwidth()
        # hs = self.winfo_screenheight()
        # x = (ws // 2) - (w // 2)
        # y = (hs // 2) - (h // 2)
        # self.geometry(f"{w}x{h}+{x}+{y}")  # устанавливаем размеры окна
        # self.minsize(w, h)

        main_menu = tk.Menu()
        file_menu = tk.Menu(tearoff=0)
        file_menu.add_command(label="Exit", command=self._exit)
        help_menu = tk.Menu(tearoff=0)
        help_menu.add_command(label="About", command=self._about)

        main_menu.add_cascade(label="File", menu=file_menu)
        main_menu.add_cascade(label="Help", menu=help_menu)
        self.config(menu=main_menu)

        self.rowconfigure(0, pad=0)
        self.rowconfigure(1, pad=0)
        self.rowconfigure(2, pad=0)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, pad=0)
        self.columnconfigure(2, weight=1)

        opts = {"padx": 5, "pady": 5, "sticky": "nswe"}

        btn = ttk.Button(
            text="Загрузить данные из файла", command=self._import
        )
        btn.grid(row=0, column=0, columnspan=4, **opts)
        self.btn_import = btn

        label = tk.Label(text="")
        label.grid(row=1, column=0, columnspan=4, **opts)
        self.label_import = label

        separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        separator.grid(row=2, column=0, columnspan=4, sticky="ew")

        label = tk.Label(self, text="Укажите период:")
        label.grid(row=3, column=0, columnspan=4, **opts)

        label = tk.Label(self, text="с:")
        label.grid(row=4, column=0, **opts)
        cal = DateEntry(self, selectmode="day")
        cal.grid(row=4, column=1, **opts)
        self.date_from = cal

        label = tk.Label(self, text="по:")
        label.grid(row=4, column=2, **opts)
        cal = DateEntry(self, selectmode="day")
        cal.grid(row=4, column=3, **opts)
        self.date_to = cal

        btn = ttk.Button(text="Сохранить данные в файл", command=self._export)
        btn.grid(row=5, column=0, columnspan=4, **opts)
        self.btn_export = btn

        label = tk.Label(text="")
        label.grid(row=6, column=0, columnspan=4, **opts)
        self.label_export = label

    def _exit(self):
        self.destroy()

    def _about(self):
        window = AboutForm(self)
        window.focus_set()
        window.grab_set()
        window.wait_window()

    def callback_import(self, msg: str):
        self.label_import.config(text=msg)
        self.update()

    def callback_export(self, msg: str):
        self.label_export.config(text=msg)
        self.update()

    def _import(self):
        filename = askopenfilename(
            title="Select a file...",
            filetypes=(
                ("xlsb", "*.xlsb"),
                ("xlsx", "*.xlsx"),
                ("All files", "*.*"),
            ),
        )

        if filename:
            self.btn_import.config(state=tk.DISABLED)
            self.config(cursor="watch")
            self.update()

            import_xlsx(
                filename=filename,
                callback_msg=self.callback_import,
            )

            self.config(cursor="")
            self.btn_import.config(state=tk.NORMAL)
            self.update()

    def _export(self):
        filename = asksaveasfilename(
            title="Select a file...",
            filetypes=(("xlsx", "*.xlsx"),),
        )

        if filename:
            self.btn_export.config(state=tk.DISABLED)
            self.config(cursor="watch")
            self.update()

            export_xlsx(
                filename=filename,
                date_from=self.date_from.get_date(),
                date_to=self.date_to.get_date(),
                callback_msg=self.callback_export,
            )

            self.btn_export.config(state=tk.NORMAL)
            self.config(cursor="")
            self.update()

            open_xlsx(filename)
