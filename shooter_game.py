
from random import randint
from pygame import *
from time import time as timer

window = display.set_mode((700, 500))
display.set_caption('Shooter')
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
clock = time.Clock()
FPS = 60
# музыка
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
mixer.music.set_volume(0.5)



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y,  player_speed):
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y,  player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1

class Bullet(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y,  player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def update(self):
        self.rect.y -= self.speed 
        if self.rect.y <0:
            self.kill()

life = 3
max_lost = 10
goal = 20
lost = 0
score = 0
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 80)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx-7, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
       
ship = Player("rocket.png", 5, 400, 80, 100, 10)
monsters = sprite.Group()

for i in range(5):
    monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(80, 620), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

bullets = sprite.Group()

win = font2.render('You WIN', 1, (255, 255, 255))
lose = font2.render('You LOSE', 1, (255, 255, 255))

reload = False
fire_num = 0

finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if fire_num < 10 and reload == False:
                    fire_num = fire_num + 1
                    fire_sound.play()
                    ship.fire()

                if fire_num >= 10 and reload == False:
                    last_time = timer()
                    reload = True

    if not finish:
        window.blit(background, (0, 0))
        text = font1.render('Счет:'+str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font1.render('Пропущено:'+str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        text_life = font2.render(str(life), True, (150, 0, 0))
        window.blit(text_life, (650, 10))
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        ship.update()
        ship.reset()
        asteroids.update()
        asteroids.draw(window)

        if reload == True:
            now_time = timer()
            if now_time - last_time <3:
                t1 = font1.render(str('Перезарядка'), 1, (150, 0, 0))
                window.blit(t1, (300, 450))
            else:
                fire_num = 0
                reload = 0


        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        bna = sprite.groupcollide(bullets, asteroids, True, False)


        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, 1)
            life -= 1
        if life ==  0 or max_lost ==  lost:
            finish = True
            window.blit(lose, (200, 200))
        elif score >= goal:
            finish = True
            window.blit(win, (200, 200))
        display.update()


    time.delay(50)
