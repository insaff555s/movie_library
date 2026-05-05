Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        ttk.Button(self.win, text="Удалить выбранный фильм", 
                   command=self.delete_movie).pack(pady=5)
    
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
