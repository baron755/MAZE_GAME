#створи гру "Лабіринт"!
from typing import Any
from pygame import *

class Gamesprite(sprite.Sprite):
    def __init__(self, img, x,y,w,h,speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (w,h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def reset(self):
        win.blit(self.image, (self.rect.x,self.rect.y))
        
class Player(Gamesprite):
    def update(self, ) -> None:
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < H-80:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < W-80:
            self.rect.x += self.speed
            
class Enemy(Gamesprite):
    direction = "left"
    
    def update(self):
        if self.rect.x <= W-150:
            self.direction = "right"
        if self.rect.x >= W-85:
            self.direction = "left"
            
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
            
class Wall(sprite.Sprite):
    def __init__(self, color, wall_x, wall_y, wall_w, wall_h):
        self.color = color
        self.width = wall_w
        self.height = wall_h
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
        
    def draw(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
            

W,H = 700,500
win = display.set_mode((W,H))
display.set_caption("Лабіринт")
clock = time.Clock()
FPS = 60
background = transform.scale(image.load("background.jpg"), (700, 500))

mixer.init()
mixer_music.load("jungles.ogg")
mixer_music.play()

kick = mixer.Sound("kick.ogg")
money = mixer.Sound("money.ogg")

font.init()
text1 = font.Font(None, 70)
text_win = text1.render("YOU WIN!",1,(0,200,0))
text_lose = text1.render("YOU LOSE!",1,(200,0,0))

game = True
finich = False

player = Player("hero.png", 5, H-80, 50, 50, 4)
enemy = Enemy("cyborg.png", W-80, H-150, 50, 50, 1)
treasure = Gamesprite("treasure.png", W-100, H-100, 65, 65, 0)

wall_1 = Wall((154,205,50), 180, 20, 450, 10)
wall_2 = Wall((154,205,50), 180, 20, 10, 350)
wall_3 = Wall((154,205,50), 180, 480, 350, 10)

wall_4 = Wall((154,205,50), 280, 125, 10, 400)
wall_5 = Wall((154,205,50), 380, 0, 10, 400)
wall_6 = Wall((154,205,50), 480, 125, 10, 400)
wall_7 = Wall((154,205,50), 480, 125, 125, 10)
wall_8 = Wall((154,205,50), 580, 225, 200, 10)
wall_9 = Wall((154,205,50), 480, 325, 125, 10)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    win.blit(background, (0, 0))

    if not finich:
        player.update()
        player.reset()
    
        enemy.update()
        enemy.reset()
    
        wall_1.draw()
        wall_2.draw()
        wall_3.draw()
        wall_4.draw()
        wall_5.draw()
        wall_6.draw()
        wall_7.draw()
        wall_8.draw()
        wall_9.draw()
    
        treasure.update()
        treasure.reset()
        
        if (sprite.collide_rect(player, enemy) or
            sprite.collide_rect(player, wall_1) or
            sprite.collide_rect(player, wall_2) or
            sprite.collide_rect(player, wall_3) or
            sprite.collide_rect(player, wall_4) or
            sprite.collide_rect(player, wall_5) or
            sprite.collide_rect(player, wall_6) or
            sprite.collide_rect(player, wall_7) or
            sprite.collide_rect(player, wall_8) or
                sprite.collide_rect(player, wall_9)):
            finich = True
            win.blit(text_lose, (200,200))
            kick.play()
            
        if sprite.collide_rect(player, treasure):
            finich = True
            win.blit(text_win, (200,200))
            money.play()
            
            
    else:
        time.delay(3000)
        player.rect.x = 5
        player.rect.y = H-80
        finich = False
        
    display.update()
    clock.tick(FPS)  