import pygame

pygame.init()
pygame.mixer.init()
pygame.font.init()

window = pygame.display.set_mode((700,500))
pygame.display.set_caption("Лабиринт")
background = pygame.transform.scale(pygame.image.load('background.jpg'), (700,500))


FPS = 60
clock = pygame.time.Clock()
font = pygame.font.Font(None, 70)
win = font.render('YOU WIN!',True, (255,215, 0))
lose = font.render('YOU LOSE!',True, (255,48,48))


pygame.mixer.music.load('jungles.ogg')
pygame.mixer.music.play()



kick = pygame.mixer.Sound('kick.ogg')
money = pygame.mixer.Sound('money.ogg')

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < 435:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
        

class Enemy(GameSprite):
    def init(self, player_image, player_x, player_y, player_speed):
        super().init(player_image, player_x, player_y, player_speed)
        self.direction = 'left'
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        if self.rect.x <= 510:
            self.direction = 'right'
        elif self.rect.x >= 635:
            self.direction = 'left'
        if self.direction ==  'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

       

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_w] and self.rect.y > 0:
        #     self.rect.y -= self.speed
        # if keys[pygame.K_s] and self.rect.y < 435:
        #     self.rect.y += self.speed
        # if keys[pygame.K_a] and self.rect.x > 0:
        #     self.rect.x -= self.speed
        # if keys[pygame.K_d] and self.rect.x < 635:
        #     self.rect.x += self.speed

class Wall(pygame.sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


hero = Player('hero.png',65,65, 5)
cyborg = Enemy('cyborg.png',510,300, 3)
treasure = GameSprite('treasure.png',550,100, 0)

walls = pygame.sprite.Group()
walls.add(Wall(97, 227, 47, 50,50,570,10))
walls.add(Wall(97, 227, 47, 200,50,10,340))
walls.add(Wall(97, 227, 47, 350,150,10,340))
walls.add(Wall(97, 227, 47, 50,480,570,10))
walls.add(Wall(97, 227, 47, 500,50,10,340))

running = True
finish = False
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not finish:
        window.blit(background,(0,0))
        walls.draw(window)

        
        cyborg.update()
        hero.update()
        hero.reset()
        cyborg.reset()
        treasure.reset()
        pygame.display.update()
        clock.tick(FPS)
        
        if pygame.sprite.collide_rect(hero, treasure):
            money.play()
            window.blit(win, (200,200))
            finish = True 
            
        if pygame.sprite.spritecollide(hero, walls, False):
            kick.play()
            window.blit(lose, (200,200))
            finish = True

                    
        if pygame.sprite.collide_rect(hero, cyborg):
            kick.play()
            window.blit(lose, (200,200))
            finish = True
            
        




    pygame.display.update()