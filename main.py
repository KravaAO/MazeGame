from pygame import *

init()
font.init()

size = (500, 500)
window = display.set_mode(size)
display.set_caption('Лабіринт')
clock = time.Clock()

class GameSprite:
    def __init__(self, img, x, y, width, height):
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = None

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= 5
        if keys[K_s] and self.rect.y < 450:
            self.rect.y += 5
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= 5
        if keys[K_d] and self.rect.x < 450:
            self.rect.x += 5

class Wall:
    def __init__(self, x, y, width, height, color):
        self.rect = Rect(x, y, width, height)
        self.color = color

    def reset(self):
        draw.rect(window, self.color, self.rect)


class Enemy(GameSprite):
    def update(self):
        if self.rect.x >= 450:
            self.direction = False
        if self.rect.x <= 240:
           self.direction = True

        if self.direction:
            self.rect.x += 5
        else:
            self.rect.x -= 5


enemy = Enemy('cyborg.png', 240, 120, 50, 50)

player = Player('hero.png', 20, 400, 50, 50)
finish = GameSprite('treasure.png', 400, 400, 50, 50)
font1 = font.Font(None, 30)

position_walls = [(100, 100), (160, 0), (220, 60), (220, 60)]
size_walls = [(5, 400), (5, 400), (5, 400), (200, 5)]

walls = list()
for i in range(len(size_walls)):
    x = position_walls[i][0]
    y = position_walls[i][1]
    width = size_walls[i][0]
    height = size_walls[i][1]
    wall = Wall(x, y, width, height, (255, 0, 0))
    walls.append(wall)

checkpoint1 = Wall(0, 20, 20, 20, (0, 255, 0))# створення стіни чекпоінту
game = True
lose = False # змінна для рестартру
checkpoint_x = 20 # перший чекпойнт позиція по x
checkpoint_y = 400 # перший чекпойнт позиція по y
hp = 3
while game:
    # Іван
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN and lose:# для рестрату клікнути мишкою по ігровому екрану
            # оновлюємо почтакові змінні
            hp = 3
            checkpoint_x = 20
            checkpoint_y = 400
            lose = False

    if not lose:
        # Женя
        window.fill((255, 255, 255))
        player.reset()
        player.update()
        finish.reset()

        for wall in walls:
            wall.reset()
            if wall.rect.colliderect(player): # перевірка чи доторкається стіна до граця
                player.rect.x = checkpoint_x
                player.rect.y = checkpoint_y
                hp -= 1

        #для ворога
        enemy.reset()
        enemy.update()
        if enemy.rect.colliderect(player):
            player.rect.x = 20
            player.rect.y = 400
            hp -= 1

        #Іван
        text_hp = font1.render(f' Життя {hp}', True, (0, 0, 0))# рендер тексту
        window.blit(text_hp, (20 , 20)) # відображення тексту та його кординати в дужкаї

        # відображення чекпоінту (можно прибрати)
        checkpoint1.reset()
        # якщо користувач доторкнувася до чекпоінту зберігаємо місце знаходження чекпоінта
        if player.rect.colliderect(checkpoint1):
            checkpoint_x = 0
            checkpoint_y = 20


    if hp <= 0:
        window.fill((255, 0, 0))
        lose = True # ми програли тому ставимо прапор lose = Правда

    if player.rect.colliderect(finish):
        window.fill((0, 255, 0))
        lose = True# ми перемогли тому ставимо прапор lose = Правда (гра закінчена)

    display.update()
    clock.tick(60)

