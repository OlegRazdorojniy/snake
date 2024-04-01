"""Calling Libraries"""
import pygame

from random import randint, choice


# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """Base class for all game objects."""

    def __init__(self, body_color=0):
        self.body_color = body_color
        self.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def draw(self):
        """Abstract method for drawing the game object."""
        pass


class Apple(GameObject):
    """Class representing an apple in the game."""

    def __init__(self, oc_cells=[], body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position(oc_cells)

    def randomize_position(self, positions):
        """Randomly assigns a position to the apple avoiding occupied cells."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in positions:
                break

    def draw(self):
        """Draws the apple on the screen."""
        rect = pygame.Rect(
            self.position,
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Class representing the snake in the game."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.last = None
        self.reset()
        self.direction = RIGHT

    def update_direction(self):
        """Updates the snake's direction if a new direction key is pressed."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Moves the snake based on its current direction."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        self.position = ((head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH,
                         (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT)
        self.positions.insert(0, self.position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Draws the snake on the screen."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                self.last,
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Getting the coordinates of the snake's head."""
        return self.positions[0]

    def reset(self):
        """Reset to original state."""
        self.length = 1
        self.positions = [self.position]
        self.directoin = choice([RIGHT, LEFT, UP, DOWN])
        self.next_direction = None


def handle_keys(game_object):
    """Handles key presses and updates the game object's direction."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """The main function of the game."""
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
