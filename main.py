# Класс для шахматной фигуры
class ChessFigure:
    # Конструктор класса (вызывается при создании фигуры)
    def __init__(self, color, name, pos):
        self.color = color  # 'w' - белые, 'b' - черные (сокращенно для экономии места)
        self.name = name    # Тип фигуры: 'p' - пешка, 'r' - ладья и т.д.
        self.pos = pos      # Текущая позиция на доске (например 'e2')
        self.moved = False  # Флаг, двигалась ли фигура (пока не используется)

    # Метод для получения символа фигуры
    def symbol(self):
        # Словарь соответствия типа фигуры и ее символа
        figures = {
            'p': 'P',  # Пешка (Pawn)
            'r': 'R',  # Ладья (Rook)
            'n': 'N',  # Конь (Knight - N для отличия от King)
            'b': 'B',  # Слон (Bishop)
            'q': 'Q',  # Ферзь (Queen)
            'k': 'K'   # Король (King)
        }
        # Для черных фигур возвращаем строчные буквы
        return figures[self.name] if self.color == 'w' else figures[self.name].lower()

# Класс для шахматной игры
class ChessGame:
    # Конструктор класса
    def __init__(self):
        self.board = {}  # Словарь для хранения фигур (ключ - позиция, значение - фигура)
        self.turn = 0    # Счетчик ходов (0 - начало игры)
        self.setup()     # Вызываем метод начальной расстановки фигур

    # Метод начальной расстановки фигур
    def setup(self):
        # Порядок фигур в начальной позиции (кроме пешек)
        figures_order = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        
        # Расставляем белые фигуры
        for i in range(8):  # Пешки на второй линии
            self.board[f"{chr(97+i)}2"] = ChessFigure('w', 'p', f"{chr(97+i)}2")
        for i, fig in enumerate(figures_order):  # Остальные фигуры на первой линии
            self.board[f"{chr(97+i)}1"] = ChessFigure('w', fig, f"{chr(97+i)}1")
        
        # Расставляем черные фигуры (аналогично белым)
        for i in range(8):  # Пешки на седьмой линии
            self.board[f"{chr(97+i)}7"] = ChessFigure('b', 'p', f"{chr(97+i)}7")
        for i, fig in enumerate(figures_order):  # Остальные фигуры на восьмой линии
            self.board[f"{chr(97+i)}8"] = ChessFigure('b', fig, f"{chr(97+i)}8")

    # Метод отображения доски
    def show(self):
        print("\n   a b c d e f g h")  # Буквы столбцов
        for row in range(8, 0, -1):    # Цикл по строкам (сверху вниз)
            line = f"{row}  "          # Номер строки
            for col in 'abcdefgh':     # Цикл по столбцам
                pos = f"{col}{row}"    # Формируем позицию (например 'a1')
                fig = self.board.get(pos)  # Получаем фигуру на этой позиции
                line += fig.symbol() + ' ' if fig else '. '  # Добавляем символ фигуры или точку
            print(line)  # Выводим строку доски
        
        # Выводим номер хода и чей сейчас ход
        print(f"\nХод: {self.turn} ({'белые' if self.turn%2==0 else 'черные'})")

    # Метод для выполнения хода
    def move(self, start, end):
        # Проверка, есть ли фигура на стартовой позиции
        if start not in self.board:
            print("Ошибка: нет фигуры на стартовой позиции")
            return False
        
        # Перемещаем фигуру
        fig = self.board[start]  # Получаем фигуру
        del self.board[start]    # Удаляем со старой позиции
        self.board[end] = fig    # Ставим на новую позицию
        fig.pos = end            # Обновляем позицию фигуры
        fig.moved = True         # Помечаем, что фигура двигалась
        self.turn += 1           # Увеличиваем счетчик ходов
        return True

# Основная функция программы
def main():
    # Выводим инструкцию
    print("Задание 1. Шахматный симулятор")
    print("Формат хода: e2 e4 (откуда куда)")
    print("Для выхода введите exit\n")
    
    # Создаем экземпляр игры
    game = ChessGame()
    player = 'w'  # Начинают белые
    
    # Основной игровой цикл
    while True:
        game.show()  # Показываем доску
        
        # Получаем ввод от пользователя
        cmd = input(f"{'Белые' if player == 'w' else 'Черные'} ходят: ").
        lower()
        
        # Проверка на выход
        if cmd == 'exit':
            break
            
        # Обработка хода
        try:
            start, end = cmd.split()  # Разделяем ввод на две позиции
            
            # Проверка формата ввода
            if len(start) != 2 or len(end) != 2:
                raise ValueError
            
            # Пытаемся сделать ход
            if game.move(start, end):
                player = 'b' if player == 'w' else 'w'  # Меняем игрока
        except:
            print("Некорректный ввод! Пример правильного ввода: e2 e4")

# Стандартная проверка для запуска программы
if __name__ == "__main__":
    main()
