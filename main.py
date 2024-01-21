import pygame
import pygame.freetype
from mapgen import mapgen
import random

size = WIDTH, HEIGHT = 1500, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
tplay1 = 1
tplay2 = 1
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
clock = pygame.time.Clock()
FPS = 10


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
    global tplay1, tplay2
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '+' and tplay1 == 1:
                Tile('Corvette_1', x, y)
            elif level[y][x] == '+' and tplay1 == 2:
                Tile('Сruiser_1', x, y)
            elif level[y][x] == '+' and tplay1 == 3:
                Tile('Battleship_1', x, y)
                battleship_blue = Battleship(x, y, 'north')
            elif level[y][x] == '-' and tplay2 == 1:
                Tile('Corvette_2', x, y)
            elif level[y][x] == '-' and tplay2 == 2:
                Tile('Сruiser_2', x, y)
            elif level[y][x] == '-' and tplay2 == 3:
                Tile('Battleship_2', x, y)
                battleship_red = Battleship(x, y, 'south')
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


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
    # image = pygame.transform.scale(image, (80, 80))
    return image


tile_images = {
    'wall': load_image('asteroid.png'),
    'empty': load_image('space.png'),
    'Corvette_1': load_image('Corvette_1.png'),
    'Corvette_2': load_image('Corvette_2.png'),
    'Сruiser_1': load_image('Сruiser_1.png'),
    'Сruiser_2': load_image('Сruiser_2.png'),
    'Battleship_1': load_image('Battleship_1.png'),
    'Battleship_2': load_image('Battleship_2.png')

}
player_image = load_image('space.png', -1)

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


class Corvette:
    pass


class Cruiser:
    pass


class Battleship:
    def __init__(self, pos_x, pos_y, dir):
        self.coord = [(pos_x, pos_y), (pos_x + 1, pos_y), (pos_x, pos_y + 1), (pos_x + 1, pos_y + 1), (pos_x, pos_y + 2),
                 (pos_x + 1, pos_y + 2)]
        self.direction = dir

    def show(self):
        return self.coord, self.direction


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


class SimpleScene:
    FONT = None
    global WIDTH, HEIGHT

    def __init__(self, next_scene, *text):
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill(pygame.Color('lightgrey'))

        y = 80
        if text:
            if SimpleScene.FONT == None:
                SimpleScene.FONT = pygame.freetype.SysFont(None, 32)
            for line in text:
                SimpleScene.FONT.render_to(self.background, (120, y), line, pygame.Color('black'))
                SimpleScene.FONT.render_to(self.background, (119, y - 1), line, pygame.Color('white'))
                y += 50

        self.next_scene = next_scene
        self.additional_text = None

    def start(self, text):
        self.additional_text = text

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        if self.additional_text:
            y = 180
            for line in self.additional_text:
                SimpleScene.FONT.render_to(screen, (120, y), line, pygame.Color('black'))
                SimpleScene.FONT.render_to(screen, (119, y - 1), line, pygame.Color('white'))
                y += 50

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return (self.next_scene, None)


class GameState:
    def __init__(self):
        global tplay1, tplay2
        self.tplay1 = tplay1
        self.tplay2 = tplay2
        print(self.tplay1, self.tplay2)
        self.questions = [
            ('How many legs has a cow?', 4),
            ('How many legs has a bird?', 2),
            ('What is 1 x 1 ?', 1)
        ]
        self.current_question = None
        self.right = 0
        self.wrong = 0
        mapgen(tplay1, tplay2)
        player, level_x, level_y = generate_level(load_level('map.txt'))
        camera = Camera()


class SettingScene_2:
    global WIDTH, HEIGHT

    def __init__(self):
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill(pygame.Color('lightgrey'))

        if SimpleScene.FONT == None:
            SimpleScene.FONT = pygame.freetype.SysFont(None, 32)
        SimpleScene.FONT.render_to(self.background, (120, 50), 'Игрок 2', pygame.Color('black'))
        SimpleScene.FONT.render_to(self.background, (120, 100), 'Выберите тоннаж корабля', pygame.Color('black'))
        SimpleScene.FONT.render_to(self.background, (120, 150),
                                   'Корветы - высокая скорость, низкие урон и броня, 8 штук', pygame.Color('black'))
        SimpleScene.FONT.render_to(self.background, (120, 200),
                                   'Крейсеры - средняя скорость, средние урон и броня, 3 штуки', pygame.Color('black'))
        SimpleScene.FONT.render_to(self.background, (120, 250),
                                   'Линкор - медленный, высокие урон и броня, множественные атаки, 1 штука',
                                   pygame.Color('black'))

        self.rects = []
        self.img = []
        self.shiplst = ['Corvette_2.png', 'Сruiser_2.png', 'Battleship_2.png']
        x = 200
        y = 350
        for n in range(3):
            rect = pygame.Rect(x, y, 80, 80)
            self.rects.append(rect)
            rect = pygame.Rect(x, y + 200, 80, 80)
            self.img.append(rect)
            x += 500

    def start(self, *args):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        n = 1
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, pygame.Color('darkgrey'), rect)
            pygame.draw.rect(screen, pygame.Color('darkgrey'), rect, 5)
            SimpleScene.FONT.render_to(screen, (rect.x + 30, rect.y + 30), str(n), pygame.Color('black'))
            SimpleScene.FONT.render_to(screen, (rect.x + 29, rect.y + 29), str(n), pygame.Color('white'))
            n += 1
        k = 0
        for img in self.rects:
            if img.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, pygame.Color('darkgrey'), img)
            pygame.draw.rect(screen, pygame.Color('darkgrey'), img, 5)
            screen.blit(pygame.transform.scale(load_image(self.shiplst[k]),
                                               (82 * (k // 2 + 1), 82 * (k % 2 + 1 + (k // 2) * 2))),
                        (img.x, img.y + 150))
            k += 1

    def update(self, events, *bkt):
        global tplay2
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                n = 1
                for rect in self.rects:
                    if rect.collidepoint(event.pos):
                        tplay2 = n
                        return ('GAME', GameState())
                    n += 1


class SettingScene_1:
    global WIDTH, HEIGHT

    def __init__(self):
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill(pygame.Color('lightgrey'))

        if SimpleScene.FONT == None:
            SimpleScene.FONT = pygame.freetype.SysFont(None, 32)
        SimpleScene.FONT.render_to(self.background, (120, 50), 'Игрок 1', pygame.Color('black'))
        SimpleScene.FONT.render_to(self.background, (120, 100), 'Выберите тоннаж корабля', pygame.Color('black'))
        SimpleScene.FONT.render_to(self.background, (120, 150),
                                   'Корветы - высокая скорость, низкие урон и броня, 8 штук', pygame.Color('black'))
        SimpleScene.FONT.render_to(self.background, (120, 200),
                                   'Крейсеры - средняя скорость, средние урон и броня, 3 штуки', pygame.Color('black'))
        SimpleScene.FONT.render_to(self.background, (120, 250),
                                   'Линкор - медленный, высокие урон и броня, множественные атаки, 1 штука',
                                   pygame.Color('black'))

        self.rects = []
        self.img = []
        self.shiplst = ['Corvette_1.png', 'Сruiser_1.png', 'Battleship_1.png']
        x = 200
        y = 350
        for n in range(3):
            rect = pygame.Rect(x, y, 80, 80)
            self.rects.append(rect)
            rect = pygame.Rect(x, y + 200, 80, 80)
            self.img.append(rect)
            x += 500

    def start(self, *args):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        n = 1
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, pygame.Color('darkgrey'), rect)
            pygame.draw.rect(screen, pygame.Color('darkgrey'), rect, 5)
            SimpleScene.FONT.render_to(screen, (rect.x + 30, rect.y + 30), str(n), pygame.Color('black'))
            SimpleScene.FONT.render_to(screen, (rect.x + 29, rect.y + 29), str(n), pygame.Color('white'))
            n += 1
        k = 0
        for img in self.rects:
            if img.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, pygame.Color('darkgrey'), img)
            pygame.draw.rect(screen, pygame.Color('darkgrey'), img, 5)
            screen.blit(pygame.transform.scale(load_image(self.shiplst[k]),
                                               (82 * (k // 2 + 1), 82 * (k % 2 + 1 + (k // 2) * 2))),
                        (img.x, img.y + 150))
            k += 1

    def update(self, events, dt):
        global tplay1
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                n = 1
                for rect in self.rects:
                    if rect.collidepoint(event.pos):
                        tplay1 = n
                        return ('PLAYER 2', SettingScene_2())
                    n += 1


class GameScene:
    global WIDTH, HEIGHT

    def __init__(self):
        if SimpleScene.FONT == None:
            SimpleScene.FONT = pygame.freetype.SysFont(None, 32)
        global tplay1, tplay2
        self.tplay1 = tplay1
        self.tplay2 = tplay2

        self.rects = []
        x = 120
        y = 120
        for n in range(4):
            rect = pygame.Rect(x, y, 80, 80)
            self.rects.append(rect)
            x += 100
        mapgen(tplay1, tplay2)
        self.player, self.level_x, self.level_y = generate_level(load_level('map.txt'))
        self.camera = Camera()

    def start(self, *args):
        pass

    def draw(self, *args):
        pass

    def update(self, events, *dt):
        STEP = 50
        global clock, FPS
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.rect.x -= STEP
                if event.key == pygame.K_RIGHT:
                    self.player.rect.x += STEP
                if event.key == pygame.K_UP:
                    self.player.rect.y -= STEP
                if event.key == pygame.K_DOWN:
                    self.player.rect.y += STEP
        # изменяем ракурс камеры
        self.camera.update(self.player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            self.camera.apply(sprite)
        screen.fill('black')
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)


def main():
    global WIDTH, HEIGHT
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    dt = 0
    scenes = {
        'TITLE': SimpleScene('PLAYER 1', 'Приветствую в игре "КОСМИЧЕКИЙ БОЙ"', '', '', '',
                             'нажмите [ПРОБЕЛ] чтобы начать'),
        'PLAYER 1': SettingScene_1(),
        'PLAYER 2': SettingScene_2(),
        'GAME': GameScene(),
        'RESULT': SimpleScene('TITLE', 'Here is your result:'),
    }
    scene = scenes['TITLE']
    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return

        result = scene.update(events, dt)
        if result:
            next_scene, state = result
            if next_scene:
                scene = scenes[next_scene]
                scene.start(state)

        scene.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
