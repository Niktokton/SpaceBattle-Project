import pygame
import sys
from mapgen import mapgen

pygame.init()
size = WIDTH, HEIGHT = 1500, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 10
clock = pygame.time.Clock()
STEP = 50
player = None
flag = 0

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

font = pygame.font.SysFont('Arial', 40)
objects = []


def load_image(name, colorkey=None):
    fullname = 'data' + '/' + name
    try:
        image = pygame.image.load(fullname).convert()
    except FileNotFoundError:
        message = f"Файл с изображением '{fullname}' не найден"
        print(message)
        raise SystemExit()
    # обесцветка
    if colorkey:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)

    # трансформация
    # image = pygame.transform.scale(image, (70, 70))
    return image


def terminate():
    pygame.quit()
    sys.exit()


def flag_up():
    global flag
    flag += 1


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpeg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру

        pygame.display.flip()
        clock.tick(FPS)


def choice_screen_first():
    global flag
    intro_text = ["ИГРОК 1", "",
                  "Выберите тоннаж корабля",
                  "Корветы - высокая скорость, низкие урон и броня, 8 штук",
                  "Крейсеры - средняя скорость, средние урон и броня, 3 штуки",
                  "Линкор - Медленный и тяжелый, высокие урон и броня, множественные атаки, 1 штука"]

    fon = pygame.transform.scale(load_image('simple.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if flag == 3:
                return  # начинаем игру

        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '+':
                Tile('Corvette_1', x, y)
            elif level[y][x] == '-':
                Tile('Corvette_2', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y



tile_images = {
    'wall': load_image('asteroid.png'),
    'empty': load_image('space.png'),
    'Corvette_1': load_image('Corvette_1.png'),
    'Corvette_2': load_image('Corvette_2.png')
}
player_image = load_image('Corvette_1.png', -1)

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


start_screen()
mapgen()
player, level_x, level_y = generate_level(load_level('map.txt'))
camera = Camera()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.rect.x -= STEP
            if event.key == pygame.K_RIGHT:
                player.rect.x += STEP
            if event.key == pygame.K_UP:
                player.rect.y -= STEP
            if event.key == pygame.K_DOWN:
                player.rect.y += STEP
    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill('black')
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(FPS)
terminate()
