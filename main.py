import pygame
import random


pygame.init()

FPS = 60
WIDTH = 1000
LENGTH = 600
BLACK = (0, 0, 0)

pygame.display.set_caption('need for speed')
sc = pygame.display.set_mode((WIDTH, LENGTH))
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 200)
sound1 = pygame.mixer.Sound('punch.wav')

car_surf = pygame.image.load('car.PNG').convert_alpha()
BLOCKS = ['block_1.PNG', 'block_2.PNG']
BLOCKS_SURF = []

for i in range(len(BLOCKS)):
    BLOCKS_SURF.append(pygame.image.load(BLOCKS[i]).convert_alpha())


class Block(pygame.sprite.Sprite):
    def __init__(self, x, surf, group, speed=5):
        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, 0))
        self.add(group)
        self.speed = speed

    def update(self):
        if self.rect.y < LENGTH:
            self.rect.y += self.speed
        else:
            self.kill()


class MainCar(pygame.sprite.Sprite):
    def __init__(self, x, y, surf):
        self.y = y
        self.x = x
        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(bottomright=(self.x, self.y))

    def draw(self):
        self.rect = self.image.get_rect(bottomright=(self.x, self.y))
        sc.blit(self.image, self.rect)

    def go_t(self):
        if self.y > 100:
            self.y -= 6

    def go_d(self):
        if self.y < LENGTH:
            self.y += 6

    def go_l(self):
        if self.x > 40:
            self.x -= 6

    def go_r(self):
        if self.x < WIDTH:
            self.x += 6


def defeat():
    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            main_game()
            return
        clock.tick(FPS)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()


def main_game():
    main_car = MainCar(WIDTH // 2, LENGTH, car_surf)
    blocks = pygame.sprite.Group()
    Block(random.randint(1, WIDTH), BLOCKS_SURF[random.randint(0, 1)], blocks, 5)
    TIME_GAME = 0
    pygame.mixer.music.load('Blinded_In_Chains.mp3')
    pygame.mixer.music.play(-1)
    while True:

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.mixer.music.pause()
                exit()
            elif i.type == pygame.USEREVENT:
                Block(random.randint(1, WIDTH), BLOCKS_SURF[random.randint(0, 1)], blocks, 5 + 0.1 * TIME_GAME)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            main_car.go_l()
        elif keys[pygame.K_d]:
            main_car.go_r()
        elif keys[pygame.K_w]:
            main_car.go_t()
        elif keys[pygame.K_s]:
            main_car.go_d()
        main_car.draw()
        blocks.draw(sc)
        pygame.display.update()
        TIME_GAME += 1 / 60
        clock.tick(FPS)
        sc.fill(BLACK)
        blocks.update()
        if pygame.sprite.spritecollideany(main_car, blocks):
            pygame.mixer.music.pause()
            sound1.play()
            clock.tick(1 / sound1.get_length())
            f1 = pygame.font.Font(None, 36)
            text1 = f1.render('your score: ' + str(round(TIME_GAME * 500)) + ' click on to continue "W"', 1,
                              (255, 255, 255))
            sc.blit(text1, (300, 200))
            pygame.display.update()
            defeat()
            return


main_game()
