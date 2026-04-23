import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from utils import measure_time
from classical import caesar_encrypt, caesar_decrypt, vigenere_encrypt, vigenere_decrypt
from math_crypto import sieve
from public_key import rsa_encrypt, rsa_decrypt
from hash_sign import simple_hash
from block_cipher import feistel_encrypt, feistel_decrypt

# ── Palette ────────────────────────────────────────────────────────────────────
BG        = "#0f1117"
SURFACE   = "#1a1d27"
SURFACE2  = "#232638"
ACCENT    = "#6c63ff"
ACCENT2   = "#a78bfa"
TEXT      = "#e8e8f0"
TEXT_DIM  = "#7a7a9a"
SUCCESS   = "#4ade80"
ERROR     = "#f87171"
BORDER    = "#2e3150"

FONT_TITLE  = ("Consolas", 13, "bold")
FONT_MONO   = ("Consolas", 11)
FONT_SMALL  = ("Consolas", 9)
FONT_LABEL  = ("Segoe UI", 10)
FONT_BTN    = ("Segoe UI", 10, "bold")


def apply_theme(root: tk.Tk):
    root.configure(bg=BG)

    style = ttk.Style(root)
    style.theme_use("clam")

    # ── Notebook ───────────────────────────────────────────────────────────────
    style.configure("TNotebook",
                    background=BG,
                    borderwidth=0,
                    tabmargins=[0, 0, 0, 0])
    style.configure("TNotebook.Tab",
                    background=SURFACE,
                    foreground=TEXT_DIM,
                    font=FONT_BTN,
                    padding=[18, 9],
                    borderwidth=0,
                    focuscolor=ACCENT)
    style.map("TNotebook.Tab",
              background=[("selected", SURFACE2)],
              foreground=[("selected", ACCENT2)])

    # ── Frame ──────────────────────────────────────────────────────────────────
    style.configure("TFrame", background=BG)
    style.configure("Card.TFrame", background=SURFACE, relief="flat")
    style.configure("Inner.TFrame", background=SURFACE2, relief="flat")

    # ── Label ──────────────────────────────────────────────────────────────────
    style.configure("TLabel",
                    background=BG,
                    foreground=TEXT,
                    font=FONT_LABEL)
    style.configure("Dim.TLabel",
                    background=SURFACE,
                    foreground=TEXT_DIM,
                    font=FONT_SMALL)
    style.configure("Section.TLabel",
                    background=SURFACE,
                    foreground=ACCENT2,
                    font=("Segoe UI", 9, "bold"))
    style.configure("Time.TLabel",
                    background=BG,
                    foreground=SUCCESS,
                    font=FONT_SMALL)
    style.configure("Title.TLabel",
                    background=BG,
                    foreground=TEXT,
                    font=FONT_TITLE)

    # ── Entry ──────────────────────────────────────────────────────────────────
    style.configure("TEntry",
                    fieldbackground=SURFACE2,
                    foreground=TEXT,
                    insertcolor=ACCENT2,
                    borderwidth=1,
                    relief="flat",
                    font=FONT_MONO)
    style.map("TEntry",
              fieldbackground=[("focus", SURFACE2)],
              bordercolor=[("focus", ACCENT)])

    # ── Separator ─────────────────────────────────────────────────────────────
    style.configure("TSeparator", background=BORDER)

    # ── Scrollbar ─────────────────────────────────────────────────────────────
    style.configure("TScrollbar",
                    background=SURFACE2,
                    troughcolor=SURFACE,
                    arrowcolor=TEXT_DIM,
                    borderwidth=0,
                    relief="flat")
    style.map("TScrollbar",
              background=[("active", BORDER)],
              arrowcolor=[("active", ACCENT2)])


def make_text_widget(parent, height=5, placeholder=""):
    frame = tk.Frame(parent, bg=SURFACE2, bd=0, highlightthickness=1,
                     highlightbackground=BORDER, highlightcolor=ACCENT)
    frame.pack(fill="x", pady=(0, 2))

    text = tk.Text(frame,
                   height=height,
                   bg=SURFACE2,
                   fg=TEXT,
                   insertbackground=ACCENT2,
                   selectbackground=ACCENT,
                   selectforeground=TEXT,
                   font=FONT_MONO,
                   bd=0,
                   padx=10,
                   pady=8,
                   wrap="word",
                   relief="flat",
                   undo=True)

    sb = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
    text.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    text.pack(side="left", fill="both", expand=True)

    if placeholder:
        text.insert("1.0", placeholder)
        text.config(fg=TEXT_DIM)

        def on_focus_in(e):
            if text.get("1.0", "end-1c") == placeholder:
                text.delete("1.0", tk.END)
                text.config(fg=TEXT)

        def on_focus_out(e):
            if not text.get("1.0", "end-1c").strip():
                text.insert("1.0", placeholder)
                text.config(fg=TEXT_DIM)

        text.bind("<FocusIn>", on_focus_in)
        text.bind("<FocusOut>", on_focus_out)

    return text


def make_entry(parent, placeholder=""):
    frame = tk.Frame(parent, bg=SURFACE2, bd=0, highlightthickness=1,
                     highlightbackground=BORDER, highlightcolor=ACCENT)
    frame.pack(fill="x", pady=(0, 2))

    entry = tk.Entry(frame,
                     bg=SURFACE2,
                     fg=TEXT,
                     insertbackground=ACCENT2,
                     selectbackground=ACCENT,
                     selectforeground=TEXT,
                     font=FONT_MONO,
                     bd=0,
                     relief="flat")
    entry.pack(fill="x", padx=10, pady=8)

    if placeholder:
        entry.insert(0, placeholder)
        entry.config(fg=TEXT_DIM)

        def on_focus_in(e):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=TEXT)

        def on_focus_out(e):
            if not entry.get().strip():
                entry.insert(0, placeholder)
                entry.config(fg=TEXT_DIM)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    return entry


def make_button(parent, text, command, style="primary"):
    colors = {
        "primary":  (ACCENT,   TEXT),
        "secondary":(SURFACE2, TEXT_DIM),
        "ghost":    (SURFACE,  TEXT_DIM),
    }
    bg_c, fg_c = colors.get(style, colors["primary"])

    btn = tk.Button(parent,
                    text=text,
                    command=command,
                    bg=bg_c,
                    fg=fg_c,
                    activebackground=ACCENT2,
                    activeforeground=TEXT,
                    font=FONT_BTN,
                    bd=0,
                    relief="flat",
                    padx=18,
                    pady=8,
                    cursor="hand2")

    def on_enter(e): btn.config(bg=ACCENT2 if style == "primary" else BORDER)
    def on_leave(e): btn.config(bg=bg_c)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


def section_label(parent, text):
    ttk.Label(parent, text=text.upper(), style="Section.TLabel").pack(
        anchor="w", pady=(10, 3))


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Шифр-Блокнот")
        self.root.geometry("960x680")
        self.root.minsize(780, 560)
        apply_theme(root)

        # ── Header ────────────────────────────────────────────────────────────
        header = tk.Frame(root, bg=SURFACE, height=54)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="⬡  ШИФР-БЛОКНОТ",
                 bg=SURFACE, fg=ACCENT2,
                 font=FONT_TITLE).pack(side="left", padx=22, pady=14)

        self._status_var = tk.StringVar(value="Готов")
        tk.Label(header, textvariable=self._status_var,
                 bg=SURFACE, fg=TEXT_DIM,
                 font=FONT_SMALL).pack(side="right", padx=22)

        # ── Notebook ──────────────────────────────────────────────────────────
        nb_wrap = tk.Frame(root, bg=BG)
        nb_wrap.pack(fill="both", expand=True, padx=0, pady=0)

        self.notebook = ttk.Notebook(nb_wrap)
        self.notebook.pack(fill="both", expand=True, padx=16, pady=12)

        self.create_classical_tab()
        self.create_math_tab()
        self.create_public_key_tab()
        self.create_hash_tab()
        self.create_block_tab()

        # ── Status bar ────────────────────────────────────────────────────────
        bar = tk.Frame(root, bg=SURFACE, height=28)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        self._time_var = tk.StringVar(value="")
        tk.Label(bar, textvariable=self._time_var,
                 bg=SURFACE, fg=SUCCESS,
                 font=FONT_SMALL).pack(side="right", padx=16)

    # ── Generic tab builder ────────────────────────────────────────────────────
    def _tab_frame(self, title: str):
        """Creates a scrollable card inside a new notebook tab."""
        outer = ttk.Frame(self.notebook)
        self.notebook.add(outer, text=title)

        canvas = tk.Canvas(outer, bg=BG, bd=0, highlightthickness=0)
        vsb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        card = tk.Frame(canvas, bg=SURFACE, padx=22, pady=18)
        win_id = canvas.create_window((0, 0), window=card, anchor="nw")

        def on_resize(e):
            canvas.itemconfig(win_id, width=e.width)

        def on_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", on_resize)
        card.bind("<Configure>", on_configure)

        # Mousewheel scroll
        def _scroll(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _scroll)

        return card

    def _build_io(self, card, input_placeholder="Введите текст…", key_hint=""):
        """Returns (input_text, key_entry, result_text)."""

        # Input block
        section_label(card, "Входные данные")
        input_text = make_text_widget(card, height=4,
                                      placeholder=input_placeholder)

        btn_row = tk.Frame(card, bg=SURFACE)
        btn_row.pack(fill="x", pady=(4, 10))
        make_button(btn_row, "📂  Загрузить файл",
                    lambda: self._load_file(input_text),
                    style="ghost").pack(side="left")

        # Key block
        section_label(card, "Ключ" + (f"  —  {key_hint}" if key_hint else ""))
        key_entry = make_entry(card, placeholder=key_hint or "Введите ключ…")

        # Result block
        section_label(card, "Результат")
        result_text = make_text_widget(card, height=4)
        result_text.config(state="disabled")

        save_row = tk.Frame(card, bg=SURFACE)
        save_row.pack(fill="x", pady=(4, 6))
        make_button(save_row, "💾  Сохранить результат",
                    lambda: self._save_file(result_text),
                    style="ghost").pack(side="left")

        return input_text, key_entry, result_text

    def _btn_row(self, card, pairs):
        """pairs = [(label, func, args_getter), ...]"""
        row = tk.Frame(card, bg=SURFACE)
        row.pack(fill="x", pady=(12, 4))
        for i, (label, func, args_fn) in enumerate(pairs):
            style = "primary" if i % 2 == 0 else "secondary"
            b = make_button(row, label,
                            lambda f=func, a=args_fn: self._run(f, a()),
                            style=style)
            b.pack(side="left", padx=(0, 8))
        return row

    # ── Runner ────────────────────────────────────────────────────────────────
    def _run(self, func, args):
        try:
            wrapped = measure_time(func)
            res, t = wrapped(*args)
            self._last_result = res

            # Update result widget (find it)
            self._current_result.config(state="normal")
            self._current_result.delete("1.0", tk.END)
            self._current_result.insert(tk.END, str(res))
            self._current_result.config(state="disabled")

            self._time_var.set(f"⏱  {t}s")
            self._status_var.set("✔  Готово")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            self._status_var.set("✖  Ошибка")

    # ── Tabs ──────────────────────────────────────────────────────────────────
    def create_classical_tab(self):
        card = self._tab_frame("🔤  Классические")
        inp, key, res = self._build_io(card,
                                       key_hint="Цезарь: число / Виженер: слово")
        self._classical_res = res

        section_label(card, "Операции")
        ops = [
            ("Цезарь  🔒  Encrypt", caesar_encrypt,
             lambda: (inp.get("1.0", tk.END).strip(), int(key.get()))),
            ("Цезарь  🔓  Decrypt", caesar_decrypt,
             lambda: (inp.get("1.0", tk.END).strip(), int(key.get()))),
            ("Виженер  🔒  Encrypt", vigenere_encrypt,
             lambda: (inp.get("1.0", tk.END).strip(), key.get().strip())),
            ("Виженер  🔓  Decrypt", vigenere_decrypt,
             lambda: (inp.get("1.0", tk.END).strip(), key.get().strip())),
        ]
        row1 = tk.Frame(card, bg=SURFACE)
        row1.pack(fill="x", pady=(8, 4))
        row2 = tk.Frame(card, bg=SURFACE)
        row2.pack(fill="x", pady=(0, 4))
        for i, (label, func, args_fn) in enumerate(ops):
            target = row1 if i < 2 else row2
            b = make_button(target, label,
                            self._make_action(func, args_fn, res),
                            style="primary" if i % 2 == 0 else "secondary")
            b.pack(side="left", padx=(0, 8), pady=2)

    def create_math_tab(self):
        card = self._tab_frame("🔢  Математика")
        inp, key, res = self._build_io(card, key_hint="Верхняя граница N")

        section_label(card, "Решето Эратосфена")
        tk.Label(card,
                 text="Находит все простые числа до N. Ключ — это и есть N.",
                 bg=SURFACE, fg=TEXT_DIM,
                 font=FONT_SMALL).pack(anchor="w", pady=(0, 8))

        row = tk.Frame(card, bg=SURFACE)
        row.pack(fill="x", pady=(4, 4))
        make_button(row, "▶  Запустить решето",
                    self._make_action(sieve, lambda: (int(key.get().strip()),), res),
                    style="primary").pack(side="left")

    def create_public_key_tab(self):
        card = self._tab_frame("🔑  Открытый ключ")
        inp, key, res = self._build_io(
            card,
            input_placeholder="Введите число…",
            key_hint="e,n  или  d,n")

        tk.Label(card,
                 text="RSA: входные данные — целое число; ключ — два числа через запятую.",
                 bg=SURFACE, fg=TEXT_DIM,
                 font=FONT_SMALL).pack(anchor="w", pady=(0, 8))

        row = tk.Frame(card, bg=SURFACE)
        row.pack(fill="x", pady=(4, 4))
        make_button(row, "RSA  🔒  Encrypt",
                    self._make_action(rsa_encrypt,
                                      lambda: (int(inp.get("1.0", tk.END)),
                                               tuple(map(int, key.get().split(",")))),
                                      res),
                    style="primary").pack(side="left", padx=(0, 8))
        make_button(row, "RSA  🔓  Decrypt",
                    self._make_action(rsa_decrypt,
                                      lambda: (int(inp.get("1.0", tk.END)),
                                               tuple(map(int, key.get().split(",")))),
                                      res),
                    style="secondary").pack(side="left")

    def create_hash_tab(self):
        card = self._tab_frame("🔐  Хеш / ЭЦП")
        inp, key, res = self._build_io(card, input_placeholder="Введите текст для хеширования…")

        tk.Label(card,
                 text="Хеш-функции необратимы — дешифровка невозможна принципиально.",
                 bg=SURFACE, fg=TEXT_DIM,
                 font=FONT_SMALL).pack(anchor="w", pady=(0, 8))

        row = tk.Frame(card, bg=SURFACE)
        row.pack(fill="x", pady=(4, 4))
        make_button(row, "#  Вычислить хеш",
                    self._make_action(simple_hash,
                                      lambda: (inp.get("1.0", tk.END).strip(),),
                                      res),
                    style="primary").pack(side="left")

    def create_block_tab(self):
        card = self._tab_frame("🧱  Блочные")
        inp, key, res = self._build_io(
            card,
            input_placeholder="Введите число…",
            key_hint="k1,k2,k3,…")

        tk.Label(card,
                 text="Сеть Фейстеля: входные данные — целое число; ключи — список через запятую.",
                 bg=SURFACE, fg=TEXT_DIM,
                 font=FONT_SMALL).pack(anchor="w", pady=(0, 8))

        row = tk.Frame(card, bg=SURFACE)
        row.pack(fill="x", pady=(4, 4))
        make_button(row, "Feistel  🔒  Encrypt",
                    self._make_action(feistel_encrypt,
                                      lambda: (int(inp.get("1.0", tk.END)),
                                               list(map(int, key.get().split(",")))),
                                      res),
                    style="primary").pack(side="left", padx=(0, 8))
        make_button(row, "Feistel  🔓  Decrypt",
                    self._make_action(feistel_decrypt,
                                      lambda: (int(inp.get("1.0", tk.END)),
                                               list(map(int, key.get().split(",")))),
                                      res),
                    style="secondary").pack(side="left")

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _make_action(self, func, args_fn, result_widget):
        """Returns a zero-arg callable that runs func and writes to result_widget."""
        def action():
            try:
                args = args_fn()
                wrapped = measure_time(func)
                res, t = wrapped(*args)

                result_widget.config(state="normal")
                result_widget.delete("1.0", tk.END)
                result_widget.insert(tk.END, str(res))
                result_widget.config(state="disabled")

                self._time_var.set(f"⏱  {t}s")
                self._status_var.set("✔  Готово")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
                self._status_var.set("✖  Ошибка")
        return action

    def _load_file(self, text_widget):
        try:
            path = filedialog.askopenfilename(
                filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
            if not path:
                return
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, content)
            text_widget.config(fg=TEXT)
            self._status_var.set(f"✔  Загружено: {path.split('/')[-1]}")
        except Exception as e:
            messagebox.showerror("Ошибка чтения", str(e))

    def _save_file(self, result_widget):
        try:
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
            if not path:
                return
            content = result_widget.get("1.0", tk.END)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self._status_var.set(f"✔  Сохранено: {path.split('/')[-1]}")
        except Exception as e:
            messagebox.showerror("Ошибка записи", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()