from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Координаты центра экрана:
START_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет объекта по умолчанию:
OBJECT_COLOR = (255, 255, 255)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

# Словарь для определения нового направления:
NEW_DIRECTION = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT
}


def handle_keys(game_object):
    """Обрабатывет нажатие клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            game_object.next_direction = NEW_DIRECTION.get(
                (game_object.direction, event.key), game_object.direction
            )


class GameObject:
    """
    Класс ИгровойОбъект

    Атрибуты
    position: tuple
        позиция объекта на поле
    body_color: tuple
        цвет объекта

    Методы
    __init__
    draw
        отрисовывает объект на поле
    draw_rect
        отрисовывает одну ячейку
    """

    def __init__(
            self, position=START_POSITION, body_color=OBJECT_COLOR
    ) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект на поле."""
        raise NotImplementedError('Method .draw() was not implemented.')

    def draw_rect(
        self, position, color=None,
        border_color=BOARD_BACKGROUND_COLOR
    ):
        """Отрисовывает одну ячейку."""
        color = color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """
    Наследник класса GameObject

    Атрибуты
    body_color: tuple
        цвет яблока
    position: tuple
        позиция яблока на поле

    Методы
    __init__
    randomize_pozition
        устанавливает позицию яблока в случайном месте поля
    draw
        отрисовывает яблоко на поле
    """

    def __init__(
        self, occupied_cells=[], position=START_POSITION,
        body_color=APPLE_COLOR
    ) -> None:
        super().__init__(position, body_color)
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells=[]):
        """Устанавливает позицию яблока в случайном месте поля."""
        x_position = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y_position = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x_position, y_position)
        if self.position in occupied_cells:
            self.randomize_position()

    def draw(self):
        """Отрисовывает яблоко на поле."""
        self.draw_rect(self.position, self.body_color, BORDER_COLOR)


class Snake(GameObject):
    """
    Наследник класса GameObject

    Атрибуты
    length: int
        длина змейки
    positions: list
        список с позициями всех элементов тела змейки
    direction: tuple
        направление движения змейки
    next_direction
        следующее направление движения
    body_color: tuple
        цвет змейки

    Методы
    __init__
    update_direction
        обновляет направление движения змейки
    move
        обновляет позицию змейки
    draw
        отрисовывает змейку на экране, затирая след
    get_head_position
        возвращает позицию головы змейки
    reset
        сбрасывает змейку в начальное состояние
    """

    def __init__(
        self, position=START_POSITION, body_color=SNAKE_COLOR
    ) -> None:
        super().__init__(position, body_color)
        self.reset()
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        x_head, y_head = self.get_head_position()
        dx, dy = self.direction
        new_x = (x_head + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (y_head + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position = (new_x, new_y)
        self.positions.insert(0, new_head_position)
        self.last = self.positions.pop() if (
            len(self.positions) > self.length) else None

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        # Отрисовка головы змейки
        self.draw_rect(self.positions[0], self.body_color, BORDER_COLOR)

        # Затирание последнего сегмента
        if self.last:
            self.draw_rect(self.last, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])


def main():
    """Обновляет сотояния обЪектов."""
    # Инициализация PyGame:
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position()
            if apple.position in snake.positions:
                break
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
            if apple.position in snake.positions:
                break
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
