import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("700x500")
        
        self.books = []
        self.file_path = "books.json"
        self.load_data()

        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # --- Секция ввода ---
        input_frame = tk.LabelFrame(self.root, text="Добавить новую книгу", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Название:").grid(row=0, column=0)
        self.ent_title = tk.Entry(input_frame)
        self.ent_title.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Автор:").grid(row=0, column=2)
        self.ent_author = tk.Entry(input_frame)
        self.ent_author.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Жанр:").grid(row=1, column=0)
        self.ent_genre = tk.Entry(input_frame)
        self.ent_genre.grid(row=1, column=1, padx=5)

        tk.Label(input_frame, text="Страниц:").grid(row=1, column=2)
        self.ent_pages = tk.Entry(input_frame)
        self.ent_pages.grid(row=1, column=3, padx=5)

        btn_add = tk.Button(input_frame, text="Добавить книгу", command=self.add_book, bg="#4CAF50", fg="white")
        btn_add.grid(row=2, column=0, columnspan=4, pady=10, sticky="we")

        # --- Секция фильтрации ---
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=5)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Жанр:").grid(row=0, column=0)
        self.filter_genre = tk.Entry(filter_frame)
        self.filter_genre.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Мин. страниц:").grid(row=0, column=2)
        self.filter_pages = tk.Entry(filter_frame)
        self.filter_pages.grid(row=0, column=3, padx=5)

        btn_filter = tk.Button(filter_frame, text="Применить", command=self.refresh_table)
        btn_filter.grid(row=0, column=4, padx=5)

        btn_reset = tk.Button(filter_frame, text="Сброс", command=self.reset_filter)
        btn_reset.grid(row=0, column=5, padx=5)

        # --- Таблица ---
        columns = ("title", "author", "genre", "pages")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страниц")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_book(self):
        title = self.ent_title.get().strip()
        author = self.ent_author.get().strip()
        genre = self.ent_genre.get().strip()
        pages = self.ent_pages.get().strip()

        if not (title and author and genre and pages):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        new_book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        }

        self.books.append(new_book)
        self.save_data()
        self.refresh_table()
        self.clear_entries()

    def refresh_table(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        genre_crit = self.filter_genre.get().lower()
        try:
            pages_crit = int(self.filter_pages.get()) if self.filter_pages.get() else 0
        except ValueError:
            pages_crit = 0

        for book in self.books:
            if genre_crit in book['genre'].lower() and book['pages'] >= pages_crit:
                self.tree.insert("", "end", values=(book['title'], book['author'], book['genre'], book['pages']))

    def reset_filter(self):
        self.filter_genre.delete(0, tk.END)
        self.filter_pages.delete(0, tk.END)
        self.refresh_table()

    def clear_entries(self):
        self.ent_title.delete(0, tk.END)
        self.ent_author.delete(0, tk.END)
        self.ent_genre.delete(0, tk.END)
        self.ent_pages.delete(0, tk.END)

    def save_data(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.books = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
