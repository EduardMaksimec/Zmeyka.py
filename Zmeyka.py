import tkinter as tk
from tkinter import messagebox
import random


class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Змейка")
        self.master.resizable(False, False)

        # Настройки игры по умолчанию
        self.cell_size = 20
        self.width = 20
        self.height = 20
        self.delay = 150  # Задержка по умолчанию (средняя сложность)
        self.score = 0
        self.direction = 'Right'
        self.game_over = False

        # Создаем холст
        self.canvas = tk.Canvas(
            self.master,
            width=self.width * self.cell_size,
            height=self.height * self.cell_size,
            bg='black'
        )
        self.canvas.pack()

        # Создаем элементы интерфейса
        self.create_widgets()

        # Инициализация игры
        self.init_game()

        # Привязываем клавиши управления
        self.master.bind('<Key>', self.change_direction)

    def create_widgets(self):
        """Создает элементы интерфейса"""
        # Фрейм для кнопок
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(fill=tk.X, padx=5, pady=5)

        # Кнопка старта
        self.start_button = tk.Button(
            self.button_frame,
            text="Старт",
            command=self.start_game
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Кнопка сброса
        self.reset_button = tk.Button(
            self.button_frame,
            text="Сброс",
            command=self.reset_game,
            state=tk.DISABLED
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Выбор сложности
        self.difficulty_label = tk.Label(
            self.button_frame,
            text="Сложность:"
        )
        self.difficulty_label.pack(side=tk.LEFT, padx=5)

        self.difficulty_var = tk.StringVar(value="medium")
        self.difficulty_menu = tk.OptionMenu(
            self.button_frame,
            self.difficulty_var,
            "easy", "medium", "hard",
            command=self.set_difficulty
        )
        self.difficulty_menu.pack(side=tk.LEFT, padx=5)

    def set_difficulty(self, difficulty):
        """Устанавливает уровень сложности"""
        difficulties = {
            "easy": 200,
            "medium": 150,
            "hard": 100
        }
        self.delay = difficulties[difficulty]

        # Если игра уже идет, обновляем задержку
        if hasattr(self, 'after_id'):
            self.master.after_cancel(self.after_id)
            self.update_game()

    def init_game(self):
        """Инициализирует игру"""
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.food = self.create_food()
        self.draw_game()

    def start_game(self):
        """Начинает игру"""
        self.start_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)
        self.difficulty_menu.config(state=tk.DISABLED)

        self.game_over = False
        self.score = 0
        self.direction = 'Right'

        self.init_game()
        self.update_game()

    def reset_game(self):
        """Сбрасывает игру"""
        if hasattr(self, 'after_id'):
            self.master.after_cancel(self.after_id)

        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.difficulty_menu.config(state=tk.NORMAL)

        self.canvas.delete("all")

    def draw_game(self):
        """Отрисовывает игровое поле"""
        self.canvas.delete("all")

        # Рисуем змею
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(
                x * self.cell_size,
                y * self.cell_size,
                (x + 1) * self.cell_size,
                (y + 1) * self.cell_size,
                fill='green',
                outline='black'
            )

        # Рисуем голову змеи другим цветом
        head_x, head_y = self.snake[0]
        self.canvas.create_rectangle(
            head_x * self.cell_size,
            head_y * self.cell_size,
            (head_x + 1) * self.cell_size,
            (head_y + 1) * self.cell_size,
            fill='darkgreen',
            outline='black'
        )

        # Рисуем еду
        food_x, food_y = self.food
        self.canvas.create_oval(
            food_x * self.cell_size,
            food_y * self.cell_size,
            (food_x + 1) * self.cell_size,
            (food_y + 1) * self.cell_size,
            fill='red',
            outline='black'
        )

    def create_food(self):
        """Создает еду в случайном месте"""
        while True:
            food = (
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1)
            )
            if food not in self.snake:
                return food

    def change_direction(self, event):
        """Изменяет направление движения змеи"""
        key = event.keysym
        if key in ['Up', 'Down', 'Left', 'Right']:
            # Запрещаем движение в противоположном направлении
            if (key == 'Up' and self.direction != 'Down') or \
                    (key == 'Down' and self.direction != 'Up') or \
                    (key == 'Left' and self.direction != 'Right') or \
                    (key == 'Right' and self.direction != 'Left'):
                self.direction = key

    def update_game(self):
        """Обновляет игровое состояние"""
        if self.game_over:
            return

        # Двигаем змею
        head_x, head_y = self.snake[0]

        if self.direction == 'Up':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + 1)
        elif self.direction == 'Left':
            new_head = (head_x - 1, head_y)
        elif self.direction == 'Right':
            new_head = (head_x + 1, head_y)

        # Проверяем столкновения
        if (new_head in self.snake or
                new_head[0] < 0 or new_head[0] >= self.width or
                new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            self.end_game()
            return

        # Добавляем новую голову
        self.snake.insert(0, new_head)

        # Проверяем, съела ли змея еду
        if new_head == self.food:
            self.score += 1
            self.food = self.create_food()
        else:
            # Удаляем хвост, если еда не съедена
            self.snake.pop()

        # Перерисовываем игру
        self.draw_game()

        # Планируем следующий ход
        self.after_id = self.master.after(self.delay, self.update_game)

    def end_game(self):
        """Завершает игру"""
        self.reset_button.config(state=tk.NORMAL)
        messagebox.showinfo("Игра окончена", f"Ваш счет: {self.score}")
        self.canvas.create_text(
            self.width * self.cell_size / 2,
            self.height * self.cell_size / 2,
            text="Игра окончена!",
            fill="white",
            font=('Arial', 20)
        )


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()