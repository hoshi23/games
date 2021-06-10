import pygame
from pygame.locals import *
import sys
import random

def make_ufo(ux,uy,situ,screen):
    ufo = pygame.image.load('ufo.png').convert_alpha()
    rect_ufo = ufo.get_rect()
    rect_ufo.center = (ux,uy)
    bakuhatsu = pygame.image.load('bakuhatsu.png').convert_alpha()
    rect_bakuhatsu = bakuhatsu.get_rect()
    rect_bakuhatsu.center = (ux,uy)
    if situ == 0:
        screen.blit(ufo,rect_ufo)
    else:
        screen.blit(bakuhatsu,rect_bakuhatsu)

def crush(shooting,ufo):  #衝突判定関数
    n = 0    #何回衝突したか
    for i in range(0,len(shooting)):
        if shooting[i][2] == 0:  #玉が残っているのか
            sx = shooting[i][0]
            sy = shooting[i][1]
            for j in range(0,len(ufo)):
                if (ufo[j][2] == 0) :
                    ux = ufo[j][0]
                    uy = ufo[j][1]
                    if (ux-42) < sx < (ux+42):
                        if (uy+10) < sy  < (uy+42):
                            shooting[i][2] = 1
                            ufo[j][2] = 1 #撃破された
                            n += 1
    return[shooting,ufo,n]


def main():
    (w,h) = (500, 800)
    pygame.init()
    pygame.display.set_mode((w,h), 0, 32)
    screen = pygame.display.get_surface()
    pygame.display.set_caption('Shooting Game')

    (x,y) = (w/2, h-100)
    player = pygame.image.load('rocket.png').convert_alpha()
    rect_player = player.get_rect()
    rect_player.center = (x,y)

    kiroku =  0   #飛行距離
    n = 0   #追撃回数

    start = pygame.font.Font('freesansbold.ttf', 150)
    start_Surface = start.render('START', True, (200, 200, 100),(0,0,100))
    start_Rect = start_Surface.get_rect()
    start_Rect.center = (w/2,h/2)

    end  = pygame.font.Font('freesansbold.ttf', 50)
    end_Surface = end.render('GAME OVER', True, (100, 200, 100), (0, 0, 100))
    end_Rect = end_Surface.get_rect()
    end_Rect.center = (w/2,200)


    enter  = pygame.font.Font('freesansbold.ttf', 40)
    enter_Surface = enter.render('Press enter key.', True, (200, 200, 200), (0, 0, 100))
    enter_Rect = enter_Surface.get_rect()
    enter_Rect.center = (w/2,h*3/4)

    r = 10  #ショットの大きさ
    v = 20  #ショットの速さ
    shooting = []  #玉の表示
    rocket_v = 5
    ufo = []
    mode = 0
    ufo_hassei  = 50

    while True:
        if mode == 0:
            shooting = []
            ufo  = []
            kiroku = 0
            n = 0
            ufo_hassei  = 50
            x = w/2
            pygame.display.update()
            pygame.time.wait(30)
            screen.fill((0,0,100,0))
            screen.blit(start_Surface, start_Rect)
            screen.blit(enter_Surface, enter_Rect)

        elif mode == 1:
            pygame.display.update()
            pygame.time.wait(30)
            screen.fill((0,0,100,0))
            rect_player.center = (x,y)
            screen.blit(player, rect_player)

            kyori = pygame.font.Font('freesansbold.ttf', 25)
            kyori_Surface = kyori.render('Flying Distance: {0}m'.format(kiroku), True, (255, 255, 255),(0,0,100))
            kyori_Rect = kyori_Surface.get_rect()
            kyori_Rect.center = (w-150,20)
            screen.blit(kyori_Surface, kyori_Rect)
            kiroku  += rocket_v

            score = pygame.font.Font('freesansbold.ttf', 25)
            score_Surface = score.render('Score: {0}'.format(n), True, (255, 255, 255),(0,0,100))
            score_Rect = kyori_Surface.get_rect()
            score_Rect.center = (w-100,45)
            screen.blit(score_Surface, score_Rect)

            if len(shooting) > 0:
                del_shooting = []
                for i in range(0,len(shooting)):
                    sx = shooting[i][0]
                    sy = shooting[i][1] - v
                    if sy >= 0:
                        if shooting[i][2] == 0:
                            pygame.draw.ellipse(screen,(255,100,0),(sx,sy,r,r))
                            shooting[i][1] = sy
                        else:
                            del_shooting.append(i)
                    else:
                        del_shooting.append(i)
                for j in range(0,len(del_shooting)):
                    del shooting[del_shooting[j]]

            pressed_key = pygame.key.get_pressed()   #プレイヤーの操作
            if pressed_key[K_LEFT]:
                rect_player.move_ip(-20,0)
                x -= 20
            if pressed_key[K_RIGHT]:
                rect_player.move_ip(20,0)
                x += 20
            if pressed_key[K_SPACE]:  #玉の発射
                sx = x
                sy = y-50
                shooting.append([sx,sy,0])

            if kiroku % 100 == 0:
                ufo_hassei += 1
                if ufo_hassei >= 200:
                    ufo_hassei = 200

            p_ufo = random.randint(0,2000)
            if p_ufo <= ufo_hassei:
                ux = random.randint(20,w-20)
                uy = 0
                p_v_ufo = random.randint(0,50)
                if p_ufo <= 20:
                    ufo_v  = 5
                elif p_ufo <= 45:
                    ufo_v = 10
                else:
                    ufo_v = 15
                ufo.append([ux,uy,0,ufo_v])
            if len(ufo) > 0:
                del_ufo = []
                for i in range(0,len(ufo)):
                    ux = ufo[i][0]
                    uy = ufo[i][1]
                    situ = ufo[i][2]
                    ufo_v = ufo[i][3]
                    if uy < h+40:
                        if situ <= 2: #倒されていない
                            make_ufo(ux,uy,situ,screen)
                            ufo[i][1] +=  ufo_v
                            if situ >= 1:
                                ufo[i][2] += 1
                        else:  #倒されてしばらくたった
                            del_ufo.append(i)
                    else:
                        mode = 2
                for j in range(0,len(del_ufo)):
                    del ufo[del_ufo[j]]

            now  = crush(shooting,ufo)
            shooting = now[0]
            ufo = now[1]
            n += now[2]

        elif mode == 2: #終わり(game over)
            pygame.display.update()
            pygame.time.wait(30)
            screen.fill((0,0,100,0))
            screen.blit(end_Surface, end_Rect)
            screen.blit(enter_Surface, enter_Rect)
            kyori = pygame.font.Font('freesansbold.ttf', 40)
            kyori_Surface = kyori.render('Flying Distance: {0}m'.format(kiroku), True, (150, 100, 255),(0,0,100))
            kyori_Rect = kyori_Surface.get_rect()
            kyori_Rect.center = (w/2,h/2)
            screen.blit(kyori_Surface, kyori_Rect)

            score = pygame.font.Font('freesansbold.ttf', 40)
            score_Surface = score.render('Score: {0}'.format(n), True, (150, 100, 255),(0,0,100))
            score_Rect = kyori_Surface.get_rect()
            score_Rect.center = (w/2,h/2+60)
            screen.blit(score_Surface, score_Rect)


        for event in pygame.event.get():
            pressed_key = pygame.key.get_pressed()
            if mode == 0:
                if pressed_key[K_RETURN]:
                    mode = 1
            elif mode == 2:
                if pressed_key[K_RETURN]:
                    mode = 0

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

main()
