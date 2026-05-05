import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("800x600")

        # Загрузка тренировок
        self.trainings = self.load_trainings()
        self.setup_ui()

    def setup_ui(self):
        # Поле ввода даты
        ttk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.date_entry = ttk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)

        # Поле выбора типа тренировки
        ttk.Label(self.root, text="Тип тренировки:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.type_var = tk.StringVar()
        training_types = ["Кардио", "Силовая", "Йога", "Растяжка", "Функциональная", "Другое"]
        self.type_combo = ttk.Combobox(self.root, textvariable=self.type_var, values=training_types, state="readonly")
        self.type_combo.grid(row=1, column=1, padx=10, pady=5)

        # Поле ввода длительности
        ttk.Label(self.root, text="Длительность (мин):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.duration_entry = ttk.Entry(self.root)
        self.duration_entry.grid(row=2, column=1, padx=10, pady=5)

        # Кнопка добавления тренировки
        self.add_btn = ttk.Button(self.root, text="Добавить тренировку", command=self.add_training)
        self.add_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # Фильтры
        ttk.Label(self.root, text="Фильтр по типу:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.filter_type_var = tk.StringVar(value="Все")
        self.filter_type_combo = ttk.Combobox(
            self.root,
            textvariable=self.filter_type_var,
            values=["Все"] + training_types
        )
        self.filter_type_combo.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.filter_date_entry = ttk.Entry(self.root)
        self.filter_date_entry.grid(row=5, column=1, padx=10, pady=5)

        self.apply_filter_btn = ttk.Button(self.root, text="Применить фильтры", command=self.refresh_trainings_table)
        self.apply_filter_btn.grid(row=6, column=0, columnspan=2, pady=5)

        # Таблица тренировок
        ttk.Label(self.root, text="Список тренировок:").grid(row=7, column=0, columnspan=2, pady=10)
        columns = ("ID", "Дата", "Тип", "Длительность (мин)")
        self.trainings_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=12)

        for col in columns:
            self.trainings_tree.heading(col, text=col)
            self.trainings_tree.column(col, width=150)

        self.trainings_tree.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Заполнение таблицы
        self.refresh_trainings_table()

    def load_trainings(self):
        if os.path.exists("trainings.json"):
            with open("trainings.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_trainings(self):
        with open("trainings.json", "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=2)

    def add_training(self):
        date_str = self.date_entry.get().strip()
        training_type = self.type_var.get()
        duration_str = self.duration_entry.get().strip()

        # Валидация даты
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД")
            return

        # Валидация длительности
        try:
            duration = int(duration_str)
            if duration <= 0:
                messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть числом")
            return

        # Проверка типа тренировки
        if not training_type:
            messagebox.showerror("Ошибка", "Выберите тип тренировки")
            return

        # Добавление тренировки
        training = {
            "id": len(self.trainings) + 1,
            "date": date_str,
            "type": training_type,
            "duration": duration
        }
        self.trainings.append(training)
        self.save_trainings()
        self.refresh_trainings_table()

        # Очистка полей ввода
        self.date_entry.delete(0, tk.END)
        self.type_var.set("")
        self.duration_entry.delete(0, tk.END)

        messagebox.showinfo("Успех", "Тренировка добавлена")

    def refresh_trainings_table(self):
        # Очистка таблицы
        for item in self.trainings_tree.get_children():
            self.trainings_tree.delete(item)

        # Получение фильтров
        filter_type = self.filter_type_var.get()
        filter_date = self.filter_date_entry.get().strip()

        filtered_trainings = self.trainings

        # Фильтр по типу тренировки
        if filter_type != "Все":
            filtered_trainings = [t for t in filtered_trainings if t["type"] == filter_type]

        # Фильтр по дате
        if filter_date:
            filtered_trainings = [t for t in filtered_trainings if t["date"] == filter_date]

        # Заполнение таблицы отфильтрованными записями
        for training in filtered_trainings:
            self.trainings_tree.insert("", "end", values=(
                training["id"],
                training["date"],
                training["type"],
                training["duration"]
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
