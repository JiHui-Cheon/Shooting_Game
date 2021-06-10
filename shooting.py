import random
from time import sleep

import pygame
from pygame.locals import *

WINDOW_WIDTH = 480 # 게임화면 가로크기
WINDOW_HEIGHT = 640 # 게임화면 세로크기

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (250, 250, 50)
RED = (250, 50, 50)

FPS = 60 # 게임 화면 초당 프레임수 60으로 설정하기

class Fighter(pygame.sprite.Sprite): # 전투기 만들기
    def __init__(self):
        super(Fighter, self).__init__()
        self.image = pygame.image.load('fighter.png') # 이미지 업로드
        self.rect = self.image.get_rect() # 우주선 갖고오기
        self.rect.x = int(WINDOW_WIDTH / 2) # 우주선 좌표찍기. 가운데
        self.rect.y = WINDOW_HEIGHT - self.rect.height # 우주선의 높이만큼 빼주기
        self.dx = 0 # 우주선이 바닥에 걸쳐있게
        self.dy = 0

    def update(self): # 비행기 움직임 처리하기
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.x < 0 or self.rect.x + self.rect.width > WINDOW_WIDTH:
        # 0보다 작으면 화면 왼쪽으로 나감./ 우주선의 위치와 우주선넓이를 더한게 화면 넓이보다 더 크면 더 넘어간다.
            self.rect.x -= self.dx

        if self.rect.y < 0 or self.rect.y + self.rect.height > WINDOW_HEIGHT:
            self.rect.y -= self.dy # 높이조절

    def draw(self, screen): # 스크린 값에 따라 그려주기
        screen.blit(self.image, self.rect)

    def collide(self, sprites): # 충돌 났을때
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite): # 충돌검사
                return sprite

class Missile(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed): # 미사일 위치값 설정
        super(Missile, self).__init__()
        self.image = pygame.image.load('missile.png') # 미사일이미지 로드
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
        self.sound = pygame.mixer.Sound('missile.wav') # 미사일발사소리

    def launch(self): # 발사소리 실행
        self.sound.play()

    def update(self): # 미사일 발사 좌표
        self.rect.y -= self.speed # 위로올라감
        if self.rect.y + self.rect.height < 0:
            self.kill() # 미사일 화면밖으로 나가면 없애기

    def collide(self, sprites): # 미사일 충돌정의
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

class Rock(pygame.sprite.Sprite): # 암석 정의
    def __init__(self, xpos, ypos, speed):
        super(Rock, self).__init__()
        rock_images = ('rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png', \
                       'rock06.png', 'rock07.png', 'rock08.png', 'rock09.png', 'rock10.png', \
                       'rock11.png', 'rock12.png', 'rock13.png', 'rock14.png', 'rock15.png', \
                       'rock16.png', 'rock17.png', 'rock19.png', 'rock19.png', 'rock20.png', \
                       'rock21.png', 'rock22.png', 'rock23.png', 'rock24.png', 'rock25.png', \
                       'rock26.png', 'rock27.png', 'rock28.png', 'rock29.png', 'rock30.png')
        self.image = pygame.image.load(random.choice(rock_images))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    def update(self):
        self.rect.y += self.speed # 내려옴

    def out_of_screen(self): # 놓치거나 파괴하면 화면밖으로 나감.
        if self.rect.y > WINDOW_HEIGHT:
            return True

def draw_text(text, font, surface, x, y, main_color): # 게임 점수 출력
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)

def occur_explosion(surface, x, y): # 폭발정의
    explosion_image = pygame.image.load('explosion.png')
    explosion_rect = explosion_image.get_rect()
    explosion_rect.x = x
    explosion_rect.y = y
    surface.blit(explosion_image, explosion_rect)

    # 폭발 소리넣어주기    
    explosion_sounds = ('explosion01.wav', 'explosion02.wav', 'explosion03.wav')
    explosion_sound = pygame.mixer.Sound(random.choice(explosion_sounds))# 랜덤으로 사운들고르기
    explosion_sound.play()

def game_loop(): # 반복해서 게임 진행되는거 기본 루프 설정하기
    default_font = pygame.font.Font('NanumGothic.ttf', 28)
    background_image = pygame.image.load('background.png')
    gameover_sound = pygame.mixer.Sound('gameover.wav')
    pygame.mixer.music.load('music.wav')
    pygame.mixer.music.play(-1) # 무한재생
    fps_clock = pygame.time.Clock()

    fighter = Fighter()
    missiles = pygame.sprite.Group()
    rocks = pygame.sprite.Group()

    occur_prob = 40
    shoot_count = 0
    count_missed = 0

    # 게임 반복문 돌리기
    done = False
    while not done: # True일때
        for event in pygame.event.get(): # 키방향키 설정, 키 누를때
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_LEFT:
                    fighter.dx -= 5
                elif event.key == pygame.K_RIGHT:
                    fighter.dx +=5
                elif event.key == pygame.K_UP:
                    fighter.dy -= 5
                elif event.key == pygame.K_DOWN:
                    fighter.dy += 5
                elif event.key == pygame.K_SPACE: # 미사일발사
                    missile = Missile(fighter.rect.centerx, fighter.rect.y, 10)
                    missile.launch()
                    missiles.add(missile)

            if event.type == pygame.KEYUP: # 키에서 손뗄때, 멈출때
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighter.dx = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    fighter.dy = 0

        screen.blit(background_image, background_image.get_rect())


        occur_of_rocks = 1 + int(shoot_count / 300) # 운석 수
        min_rock_speed = 1 + int(shoot_count / 200)
        max_rock_speed = 1 + int(shoot_count / 100)

        if random.randint(1, occur_prob) == 1:
            for i in range(occur_of_rocks):
                speed = random.randint(min_rock_speed, max_rock_speed)
                rock = Rock(random.randint(0, WINDOW_WIDTH - 30), 0, speed)
                rocks.add(rock)

        draw_text('파괴한 운석: {}'.format(shoot_count), default_font, screen, 100, 20, YELLOW)
        draw_text('놓친 운석: {}'.format(count_missed), default_font, screen, 400, 20, RED)

        for missile in missiles: # 발사된 미사일의 충돌체크하기
            rock = missile.collide(rocks)
            if rock:
                missile.kill()
                rock.kill()
                occur_explosion(screen, rock.rect.x, rock.rect.y)
                shoot_count += 1
        
        for rock in rocks: # 돌 화면밖으로 나갔을 때 설정하기
            if rock.out_of_screen():
                rock.kill()
                count_missed += 1

        rocks.update()
        rocks.draw(screen)
        missiles.update()
        missiles.draw(screen)
        fighter.update()
        fighter.draw(screen)
        pygame.display.flip() # 업뎃값 전체반영

        # 게임 끝나는 조건 반영


        if fighter.collide(rocks) or count_missed >= 3: # 3개 이상 놓쳤을때
            pygame.mixer_music.stop() # 음악 꺼주기
            occur_explosion(screen, fighter.rect.x, fighter.rect.y)
            pygame.display.update()
            gameover_sound.play()
            sleep(1) # 잠깐쉬기
            done = True # 반복문 끝남.

        fps_clock.tick(FPS)

    return 'game_menu' # 게임 메뉴로 돌아가기

def game_menu():
    start_image = pygame.image.load('background.png')
    screen.blit(start_image, [0, 0])
    draw_x = int(WINDOW_WIDTH / 2)
    draw_y = int(WINDOW_HEIGHT / 4)
    font_70 = pygame.font.Font('NanumGothic.ttf', 70)
    font_40 = pygame.font.Font('NanumGothic.ttf', 40)

    draw_text('지구를 지켜라!', font_70, screen, draw_x, draw_y, YELLOW)
    draw_text('엔터 키를 누르면', font_40, screen, draw_x, draw_y + 200, WHITE)
    draw_text('게임이 시작됩니다.', font_40, screen, draw_x, draw_y + 250, WHITE)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: # 엔터값
                return 'play'
        if event.type == QUIT:
                return 'quit'

    return 'game_menu'

def main():
    global screen

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("JIHUI's PyShooting!")

    action = 'game_menu'
    while action != 'quit':
        if action == 'game_menu':
            action = game_menu()
        elif action == 'play':
            action = game_loop() # 게임 수행중

    pygame.quit()

if __name__ == "__main__":
    main()