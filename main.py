import tkinter as tk
from tkinter import ttk, messagebox
import json, os

class MovieLibrary:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Movie Library")
        self.win.geometry("700x550")
        self.movies = self.load_json("movies.json")
        self.filtered_movies = self.movies.copy()
        self.init_ui()
        self.update_table()

    def load_json(self, filename):
        try:
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
        return []

    def save_json(self, filename, data):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

    def init_ui(self):
        ttk.Label(self.win, text="Movie Library", font=("Arial", 16, "bold")).pack(pady=10)
        add_frame = ttk.LabelFrame(self.win, text="Добавить фильм", padding=10)
        add_frame.pack(fill="x", padx=20, pady=5)
        ttk.Label(add_frame, text="Название:").grid(row=0, column=0, sticky="w", pady=3)
        self.entry_title = ttk.Entry(add_frame, width=30)
        self.entry_title.grid(row=0, column=1, padx=10, pady=3)
        ttk.Label(add_frame, text="Жанр:").grid(row=1, column=0, sticky="w", pady=3)
        self.entry_genre = ttk.Entry(add_frame, width=30)
        self.entry_genre.grid(row=1, column=1, padx=10, pady=3)
        ttk.Label(add_frame, text="Год выпуска:").grid(row=2, column=0, sticky="w", pady=3)
        self.entry_year = ttk.Entry(add_frame, width=10)
        self.entry_year.grid(row=2, column=1, padx=10, pady=3, sticky="w")
        ttk.Label(add_frame, text="Рейтинг (0-10):").grid(row=3, column=0, sticky="w", pady=3)
        self.entry_rating = ttk.Entry(add_frame, width=10)
        self.entry_rating.grid(row=3, column=1, padx=10, pady=3, sticky="w")
        ttk.Button(add_frame, text="Добавить фильм", command=self.add_movie).grid(row=4, columnspan=2, pady=10)
        filter_frame = ttk.LabelFrame(self.win, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=20, pady=5)
        ttk.Label(filter_frame, text="По жанру:").grid(row=0, column=0, sticky="w")
        self.filter_genre = ttk.Combobox(filter_frame, width=20, state="readonly")
        self.filter_genre.grid(row=0, column=1, padx=5)
        self.filter_genre.bind("<<ComboboxSelected>>", lambda e: self.apply_filter())
        ttk.Label(filter_frame, text="По году:").grid(row=0, column=2, sticky="w", padx=(10,0))
        self.filter_year = ttk.Entry(filter_frame, width=10)
        self.filter_year.grid(row=0, column=3, padx=5)
        ttk.Button(filter_frame, text="Фильтр", command=self.apply_filter).grid(row=0, column=4, padx=5)
        ttk.Button(filter_frame, text="Сброс", command=self.reset_filter).grid(row=0, column=5, padx=5)
        table_frame = ttk.Frame(self.win)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")
        self.tree.column("title", width=250)
        self.tree.column("genre", width=150)
        self.tree.column("year", width=80)
        self.tree.column("rating", width=80)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        ttk.Button(self.win, text="Удалить выбранный фильм", command=self.delete_movie).pack(pady=5)

    def add_movie(self):
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        year_str = self.entry_year.get().strip()
        rating_str = self.entry_rating.get().strip()
        if not title or not genre:
            messagebox.showerror("Ошибка", "Название и жанр не могут быть пустыми!")
            return
        try:
            year = int(year_str)
            if year < 1888 or year > 2030:
                messagebox.showerror("Ошибка", "Год должен быть от 1888 до 2030!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом!")
            return
        movie = {"title": title, "genre": genre, "year": year, "rating": rating}
        self.movies.append(movie)
        self.save_json("movies.json", self.movies)
        self.entry_title.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_rating.delete(0, tk.END)
        self.apply_filter()
        messagebox.showinfo("Готово", f"Фильм '{title}' добавлен!")

    def apply_filter(self):
        genre_filter = self.filter_genre.get()
        year_filter = self.filter_year.get().strip()
        self.filtered_movies = self.movies.copy()
        if genre_filter and genre_filter != "Все":
            self.filtered_movies = [m for m in self.filtered_movies if m["genre"] == genre_filter]
        if year_filter:
            try:
                year = int(year_filter)
                self.filtered_movies = [m for m in self.filtered_movies if m["year"] == year]
            except ValueError:
                pass
        self.update_table()

    def reset_filter(self):
        self.filter_genre.set("Все")
        self.filter_year.delete(0, tk.END)
        self.filtered_movies = self.movies.copy()
        self.update_table()

    def update_table(self):
        genres = sorted(set(m["genre"] for m in self.movies))
        self.filter_genre["values"] = ["Все"] + genres
        if not self.filter_genre.get():
            self.filter_genre.set("Все")
        for item in self.tree.get_children():
            self.tree.delete(item)
        for movie in self.filtered_movies:
            self.tree.insert("", "end", values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def delete_movie(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите фильм для удаления!")
            return
        item = self.tree.item(selected[0])
        title = item["values"][0]
        if messagebox.askyesno("Подтверждение", f"Удалить фильм '{title}'?"):
            self.movies = [m for m in self.movies if m["title"] != title]
            self.save_json("movies.json", self.movies)
            self.apply_filter()

    def run(self):
        self.win.mainloop()

if __name__ == "__main__":
    MovieLibrary().run()
