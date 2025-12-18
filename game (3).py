import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB = "games_final.db"

# =====================================================
# DATABASE
# =====================================================
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        genre TEXT,
        platform TEXT,
        year INTEGER,
        rating INTEGER
    );
    """)
    conn.commit()
    conn.close()


def insert_game(name, genre, platform, year, rating):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO games (name, genre, platform, year, rating) VALUES (?, ?, ?, ?, ?)",
              (name, genre, platform, year, rating))
    conn.commit()
    conn.close()


def update_game(id_game, name, genre, platform, year, rating):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    UPDATE games SET name=?, genre=?, platform=?, year=?, rating=? WHERE id=?
    """, (name, genre, platform, year, rating, id_game))
    conn.commit()
    conn.close()


def delete_game(id_game):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM games WHERE id=?", (id_game,))
    conn.commit()
    conn.close()


def load_all_games():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM games")
    rows = c.fetchall()
    conn.close()
    return rows


# =====================================================
# GUI
# =====================================================
class GameApp:

    def __init__(self, root):
        self.root = root
        root.title("Game Manager - Dark Purple Version")
        root.geometry("900x600")
        root.configure(bg="#1a0b1f") # dark purple background

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2c1240",
                        foreground="white",
                        rowheight=28,
                        fieldbackground="#2c1240")
        style.map("Treeview", background=[("selected", "#ff4dd2")]) # pink select

        title = tk.Label(root, text="Game Manager (CRUD)",
                         font=("Segoe UI", 20, "bold"),
                         fg="#ff82e6", bg="#1a0b1f")
        title.pack(pady=10)

        form_frame = tk.Frame(root, bg="#1a0b1f")
        form_frame.pack(pady=10)

        # ----------- FORM LABELS + ENTRIES -----------
        lbl_color = "white"
        entry_bg = "#3a1550"
        entry_fg = "white"

        tk.Label(form_frame, text="Name:", fg=lbl_color, bg="#1a0b1f").grid(row=0, column=0, padx=5, pady=5)
        self.name_ent = tk.Entry(form_frame, bg=entry_bg, fg=entry_fg)
        self.name_ent.grid(row=0, column=1, padx=5)

        tk.Label(form_frame, text="Genre:", fg=lbl_color, bg="#1a0b1f").grid(row=1, column=0, padx=5, pady=5)
        self.genre_ent = tk.Entry(form_frame, bg=entry_bg, fg=entry_fg)
        self.genre_ent.grid(row=1, column=1, padx=5)

        tk.Label(form_frame, text="Platform:", fg=lbl_color, bg="#1a0b1f").grid(row=2, column=0, padx=5, pady=5)
        self.platform_ent = tk.Entry(form_frame, bg=entry_bg, fg=entry_fg)
        self.platform_ent.grid(row=2, column=1, padx=5)

        tk.Label(form_frame, text="Year:", fg=lbl_color, bg="#1a0b1f").grid(row=3, column=0, padx=5, pady=5)
        self.year_ent = tk.Entry(form_frame, bg=entry_bg, fg=entry_fg)
        self.year_ent.grid(row=3, column=1, padx=5)

        tk.Label(form_frame, text="Rating:", fg=lbl_color, bg="#1a0b1f").grid(row=4, column=0, padx=5, pady=5)
        self.rating_ent = tk.Entry(form_frame, bg=entry_bg, fg=entry_fg)
        self.rating_ent.grid(row=4, column=1, padx=5)

        # ---------- BUTTONS ----------
        btn_frame = tk.Frame(root, bg="#1a0b1f")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Create (Ezafe)",
                  bg="#ff4dd2", fg="black", width=12,
                  command=self.btn_create).grid(row=0, column=0, padx=8)

        tk.Button(btn_frame, text="Update (Virayesh)",
                  bg="#d966ff", fg="black", width=12,
                  command=self.btn_update).grid(row=0, column=1, padx=8)

        tk.Button(btn_frame, text="Delete (Hazf)",
                  bg="#ff1a75", fg="white", width=12,
                  command=self.btn_delete).grid(row=0, column=2, padx=8)

        tk.Button(btn_frame, text="Refresh",
                  bg="#b84dff", fg="black", width=12,
                  command=self.refresh_list).grid(row=0, column=3, padx=8)

        # ---------- TREEVIEW ----------
        self.tree = ttk.Treeview(root, columns=("no", "name", "genre", "plat", "year", "rate"),
                                 show="headings", height=12)
        self.tree.pack(pady=20, fill="x")

        for col in ("no", "name", "genre", "plat", "year", "rate"):
            self.tree.heading(col, text=col.upper())

        self.tree.bind("<Double-1>", self.on_row_select)

        self.refresh_list()

    # =====================================================
    # CRUD BUTTONS
    # =====================================================

    def btn_create(self):
        name = self.name_ent.get()
        genre = self.genre_ent.get()
        plat = self.platform_ent.get()
        year = self.year_ent.get()
        rating = self.rating_ent.get()

        if name == "":
            messagebox.showerror("Khata", "Name khali ast.")
            return

        insert_game(name, genre, plat, year, rating)
        self.refresh_list()
        messagebox.showinfo("OK", "Game jadid ezafe shod!")

    def btn_update(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Khata", "Hich item entekhab nashode.")
            return

        values = self.tree.item(selected)["values"]

        game_id = self.get_db_id(values[0])

        update_game(
            game_id,
            self.name_ent.get(),
            self.genre_ent.get(),
            self.platform_ent.get(),
            self.year_ent.get(),
            self.rating_ent.get()
        )
        self.refresh_list()
        messagebox.showinfo("OK", "Game update shod.")

    def btn_delete(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Khata", "Item entekhab kon.")
            return

        values = self.tree.item(selected)["values"]
        game_id = self.get_db_id(values[0])

        if messagebox.askyesno("Delete", "Motma'eni hazf konam?"):
            delete_game(game_id)
            self.refresh_list()

    def on_row_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected)["values"]

        # load to form
        self.name_ent.delete(0, tk.END)
        self.genre_ent.delete(0, tk.END)
        self.platform_ent.delete(0, tk.END)
        self.year_ent.delete(0, tk.END)
        self.rating_ent.delete(0, tk.END)

        game_id = self.get_db_id(values[0])
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT * FROM games WHERE id=?", (game_id,))
        row = c.fetchone()
        conn.close()

        if row:
            self.name_ent.insert(0, row[1])
            self.genre_ent.insert(0, row[2])
            self.platform_ent.insert(0, row[3])
            self.year_ent.insert(0, row[4])
            self.rating_ent.insert(0, row[5])

    # =====================================================
    # HELPER
    # =====================================================
    def get_db_id(self, row_number):

        games = load_all_games()
        if 0 < row_number <= len(games):
            return games[row_number - 1][0]
        return None

    def refresh_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        games = load_all_games()
        for i, row in enumerate(games, start=1):

            self.tree.insert("", "end", values=(i, row[1], row[2], row[3], row[4], row[5]))


# =====================================================
# START APP
# =====================================================
init_db()
root = tk.Tk()
GameApp(root)
root.mainloop()