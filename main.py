"""
Шахматная игра на Python
Реализация включает три основных класса:
1. ChessPiece - представляет шахматную фигуру
2. ChessBoard - представляет шахматную доску и логику игры
3. ChessGame - управляет игровым процессом
"""

class ChessPiece:
    """Класс, представляющий шахматную фигуру"""
    def __init__(self, color, symbol):
        """
        Конструктор фигуры
        :param color: 'white' или 'black' - цвет фигуры
        :param symbol: символьное обозначение фигуры (p, r, n, b, q, k и их заглавные версии)
        """
        self.color = color  # Цвет фигуры
        self.symbol = symbol  # Символ для отображения

    def __str__(self):
        """Строковое представление фигуры (возвращает символ)"""
        return self.symbol

    def is_valid_move(self, board, start, end):
        """
        Проверка, является ли ход допустимым для данной фигуры
        В текущей реализации всегда True (упрощенная версия)
        В полной реализации должен проверять правила движения для конкретного типа фигуры
        """
        return True


class ChessBoard:
    """Класс, представляющий шахматную доску и логику перемещения фигур"""
    def __init__(self):
        """Инициализация доски - создаем пустую доску и расставляем фигуры"""
        self.board = self.initialize_board()  # Инициализируем доску
        self.move_count = 0  # Счетчик ходов (пока не используется)

    def initialize_board(self):
        """Создание начальной расстановки фигур на доске"""
        # Создаем пустую доску 8x8 (каждая клетка изначально None)
        empty_row = [None] * 8  # Пустая строка
        board = [empty_row[:] for _ in range(8)]  # 8 пустых строк

        # Расставляем пешки
        for i in range(8):
            board[1][i] = ChessPiece('black', 'p')  # Черные пешки на второй строке
            board[6][i] = ChessPiece('white', 'P')  # Белые пешки на седьмой строке

        # Расставляем ладьи
        board[0][0] = board[0][7] = ChessPiece('black', 'r')  # Черные ладьи
        board[7][0] = board[7][7] = ChessPiece('white', 'R')  # Белые ладьи

        # Расставляем коней
        board[0][1] = board[0][6] = ChessPiece('black', 'n')  # Черные кони
        board[7][1] = board[7][6] = ChessPiece('white', 'N')  # Белые кони

        # Расставляем слонов
        board[0][2] = board[0][5] = ChessPiece('black', 'b')  # Черные слоны
        board[7][2] = board[7][5] = ChessPiece('white', 'B')  # Белые слоны

        # Расставляем ферзей
        board[0][3] = ChessPiece('black', 'q')  # Черный ферзь
        board[7][3] = ChessPiece('white', 'Q')  # Белый ферзь

        # Расставляем королей
        board[0][4] = ChessPiece('black', 'k')  # Черный король
        board[7][4] = ChessPiece('white', 'K')  # Белый король

        return board

    def display(self):
        """Отображение текущего состояния доски в консоли"""
        print("  a b c d e f g h")  # Буквенные обозначения столбцов
        for row_index, row in enumerate(self.board):
            print(8 - row_index, end=" ")  # Номера строк (от 8 до 1)
            for cell in row:
                # Выводим символ фигуры или точку, если клетка пуста
                print(cell.symbol if cell else '.', end=" ")
            print()  # Переход на новую строку
        print()  # Пустая строка после доски

    def move_piece(self, start, end):
        """
        Попытка перемещения фигуры с проверкой допустимости хода
        :param start: начальная позиция (кортеж (row, col))
        :param end: конечная позиция (кортеж (row, col))
        :return: True, если ход выполнен, False, если ход недопустим
        """
        start_row, start_col = start  # Распаковываем координаты начала
        end_row, end_col = end       # Распаковываем координаты конца

        # Получаем фигуру в начальной позиции
        piece = self.board[start_row][start_col]

        # Проверка 1: Есть ли фигура в начальной позиции?
        if not piece:
            print("No piece at the starting position.")
            return False

        # Проверка 2: Допустим ли такой ход для этой фигуры?
        if not piece.is_valid_move(self.board, start, end):
            print("Invalid move for this piece.")
            return False

        # Получаем фигуру в конечной позиции (если есть)
        target_piece = self.board[end_row][end_col]

        # Проверка 3: Не пытаемся ли съесть свою фигуру?
        if target_piece and target_piece.color == piece.color:
            print("Cannot capture your own piece.")
            return False

        # Если все проверки пройдены - выполняем ход
        self.board[end_row][end_col] = piece  # Ставим фигуру на новое место
        self.board[start_row][start_col] = None  # Убираем фигуру со старого места
        self.move_count += 1  # Увеличиваем счетчик ходов
        return True


class ChessGame:
    """Класс, управляющий игровым процессом"""
    def __init__(self):
        """Инициализация игры - создаем доску и устанавливаем первый ход за белыми"""
        self.board = ChessBoard()  # Создаем экземпляр доски
        self.current_turn = 'white'  # Первыми ходят белые

    def parse_position(self, position):
        """
        Преобразование шахматной нотации (например, 'e2') в индексы матрицы
        :param position: строка с позицией (например, 'e2')
        :return: кортеж (row, col) или None, если ввод некорректен
        """
        # Проверка корректности ввода
        if len(position) != 2 or position[0] not in 'abcdefgh' or position[1] not in '12345678':
            return None

        # Преобразование буквы в номер столбца (a=0, b=1, ..., h=7)
        col = ord(position[0]) - ord('a')
        
        # Преобразование цифры в номер строки (1=7, 2=6, ..., 8=0)
        row = 8 - int(position[1])
        
        return row, col

    def play(self):
        """Основной игровой цикл"""
        while True:  # Бесконечный цикл игры
            # Показываем текущее состояние доски
            self.board.display()
            
            # Объявляем, чей сейчас ход
            print(f"Ход {'Белых' if self.current_turn == 'white' else 'Черных'}")

            # Запрос начальной позиции
            start = input("Введите позицию фигуры для хода (например, e2): ")
            start = self.parse_position(start)
            if not start:  # Если ввод некорректен
                print("Неверный ввод. Попробуйте снова.")
                continue  # Повторяем запрос

            # Запрос конечной позиции
            end = input("Введите целевую позицию (например, e4): ")
            end = self.parse_position(end)
            if not end:  # Если ввод некорректен
                print("Неверный ввод. Попробуйте снова.")
                continue

            # Пытаемся сделать ход
            if self.board.move_piece(start, end):
                # Если ход успешен - меняем игрока
                self.current_turn = 'black' if self.current_turn == 'white' else 'white'


if __name__ == "__main__":
    """Точка входа в программу"""
    game = ChessGame()  # Создаем экземпляр игры
    game.play()         # Запускаем игровой цикл

