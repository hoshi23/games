import pygame
from pygame.locals import *
import sys
import random

def court_point(now,cw,ch,cs,cu,cw0,ch0):  #コート番号からコート位置の特定(enemy)
    (x0,y0) = (now[1],now[2])
    if now[0] == 1:  #敵コート側
        enemy_x = [cw0-cw/4,cw0+cw/4]
        enemy_y = [ch0-ch/2+cu/2,ch0-cs-cu/2,ch0-cs/2]
        (x,y) = (enemy_x[x0], enemy_y[y0])
    else:  #プレイヤー側コート
        player_x = [cw0+cw/4,cw0-cw/4]
        player_y = [ch0+ch/2-cu/2,ch0+cs+cu/2,ch0+cs/2]
        (x,y) = (player_x[x0], player_y[y0])
    return (x,y)

def make_aim(aim,cw,ch,cs,cu,cw0,ch0,screen): #狙うところの選択
    (x,y) = court_point(aim,cw,ch,cs,cu,cw0,ch0)
    w  = cw/2
    if aim[2] == 2:
        h = cs
    else:
        h = cu
    if aim[0] == 1:
        pygame.draw.rect(screen,(0,100,100),Rect(x-w/2,y-h/2,w,h))
    else:
        pygame.draw.rect(screen,(100,100,0),Rect(x-w/2,y-h/2,w,h))

def inverse_court_point(x,y,cw,ch,cs,cu,cw0,ch0):  #座標からコート位置
    now = [0,0,0]
    if y < ch0:
        now[0] = 1
    if (x <= cw0):
        now[1] = 1
    else:
        now[1] = 0
    if (y <= ch0+cs):
        now[2] = 2
    elif (y <= ch0+cs+cu):
        now[2] = 1
    else:
        now[2] = 0
    return now

def movement(before,after,v,cw,ch,cs,cu,cw0,ch0): #速度決定,vは速さ
    (b_x,b_y) = court_point(before,cw,ch,cs,cu,cw0,ch0)  #飛ばす前
    (a_x,a_y) = court_point(after,cw,ch,cs,cu,cw0,ch0)  #飛ばす後
    (vx0,vy0) = (a_x-b_x , a_y-b_y)
    kyori = (vx0**2 + vy0**2) ** (1/2)
    if kyori == 0:
        (vx,vy)  = (0,0)
    else:
        (vx,vy) = (vx0/kyori*v, vy0/kyori*v)
    return (vx,vy)

def main():
    (w,h) = (600, 800)
    pygame.init()
    pygame.display.set_mode((w,h), 0, 32)
    screen = pygame.display.get_surface()
    pygame.display.set_caption('Badminton Game')

    mode = 0
    (cw,ch,cs) = (5.18*40, 13.5*40, 1.98*40)  #コート大きさ,サービスラインとネットの距離
    cu = (ch/2-cs)/2
    (cw0,ch0) = (w/2,h/2+50)  #コートの真ん中
    line_wide = 5  #線の太さ
    sv = 10 #シャトルの速さの基本段階
    ev = 10 #敵の移動速度
    aim = [0,0]
    rally = 0  #先行はプレイヤーから
    game = 21  #勝利ポイント


    start = pygame.font.Font('freesansbold.ttf', 150)
    start_Surface = start.render('START', True, (200, 200, 100),(0,0,0))
    start_Rect = start_Surface.get_rect()
    start_Rect.center = (w/2,h/2)

    enter  = pygame.font.Font('freesansbold.ttf', 40)
    enter_Surface = enter.render('Press enter key.', True, (200, 200, 200), (0, 0, 0))
    enter_Rect = enter_Surface.get_rect()
    enter_Rect.center = (w/2,h-50)

    gameset = pygame.font.Font('freesansbold.ttf', 70)
    gameset_Surface = gameset.render('GAME!!', True, (0, 100, 100),(0,0,0))
    gameset_Rect = gameset_Surface.get_rect()
    gameset_Rect.center = (w/2,h/4)

    win = pygame.font.Font('freesansbold.ttf', 50)
    win_Surface = win.render('YOU WIN', True, (255, 0, 0),(0,0,0))
    win_Rect = win_Surface.get_rect()
    win_Rect.center = (w/2,h/2+200)

    lose = pygame.font.Font('freesansbold.ttf', 50)
    lose_Surface = lose.render('YOU LOSE', True, (0, 0, 255),(0,0,0))
    lose_Rect = lose_Surface.get_rect()
    lose_Rect.center = (w/2,h/2+200)

    you  = pygame.font.Font('freesansbold.ttf', 50)
    you_Surface = you.render('you', True, (0, 100, 100), (0, 0, 0))
    you_Rect = you_Surface.get_rect()
    you_Rect.center = (w/2,h-40)

    enemy = pygame.image.load("sports_badminton_racket.png").convert_alpha()
    rect_enemy = enemy.get_rect()
    (ew,eh) = (int(enemy.get_width() / 2),int(enemy.get_height() / 2))

    player = pygame.image.load("sports_badminton_racket.png").convert_alpha()
    rect_player = player.get_rect()
    (pw,ph) = (int(player.get_width() / 2),int(player.get_height() / 2))

    shuttle = pygame.image.load("shuttle.png").convert_alpha()
    rect_shuttle = shuttle.get_rect()
    (sw,sh) = (int(shuttle.get_width() / 2),int(shuttle.get_height() / 2))



    while True:
        pygame.display.update()
        pygame.time.wait(30)
        screen.fill((0,0,0,0))
        pressed_key = pygame.key.get_pressed()
        if mode == 0:  #スタート
            if pressed_key[K_RETURN]:
                mode = 1
            else:
                screen.blit(start_Surface, start_Rect)
                screen.blit(enter_Surface, enter_Rect)
                (enemy_point, player_point) = (0,0)

        elif mode == 1 or mode == 2:  #プレイ中
            if (player_point == game) or (enemy_point == game):  #どちらかの勝利で終了
                mode = 3
            else:
                sub_aim = [1,aim[0],aim[1]]
                dis_point = pygame.font.Font('freesansbold.ttf', 50)
                dis_point_Surface = dis_point.render('{0} - {1}'.format(player_point, enemy_point), True, (255, 255, 255),(0,0,0))
                dis_point_Rect = dis_point_Surface.get_rect()
                dis_point_Rect.center = (w/2,50)
                screen.blit(dis_point_Surface, dis_point_Rect)
                make_aim(sub_aim,cw,ch,cs,cu,cw0,ch0,screen)
                if rally == 1:
                    make_aim(after,cw,ch,cs,cu,cw0,ch0,screen)
                pygame.draw.line(screen,(255,255,255),(cw0-cw/2,ch0-ch/2),(cw0+cw/2,ch0-ch/2),line_wide)
                pygame.draw.line(screen,(255,255,255),(cw0-cw/2,ch0-ch/2),(cw0-cw/2,ch0+ch/2),line_wide)
                pygame.draw.line(screen,(255,255,255),(cw0+cw/2,ch0+ch/2),(cw0+cw/2,ch0-ch/2),line_wide)
                pygame.draw.line(screen,(255,255,255),(cw0+cw/2,ch0+ch/2),(cw0-cw/2,ch0+ch/2),line_wide)
                pygame.draw.line(screen,(255,255,255),(cw0,ch0-ch/2),(cw0,ch0-cs),line_wide)
                pygame.draw.line(screen,(255,255,255),(cw0,ch0+ch/2),(cw0,ch0+cs),line_wide)
                pygame.draw.line(screen,(255,255,255),(cw0-cw/2,ch0-cs),(cw0+cw/2,ch0-cs),line_wide)
                pygame.draw.line(screen,(255,255,255),(cw0-cw/2,ch0+cs),(cw0+cw/2,ch0+cs),line_wide)
                pygame.draw.line(screen,(100,255,100),(cw0-cw/2-50,ch0),(cw0+cw/2+50,ch0),line_wide)
                screen.blit(you_Surface, you_Rect)

                if mode == 1: #サーブ待機
                    aim = [0,0]
                    (vex,vey) = (0,0)
                    e_stop = 0
                    if rally == 0:  #プレイヤー側のサーブ
                        pygame.draw.ellipse(screen,(255,0,0),(w/4+30,40,25,25))
                        if player_point %2 == 0:
                            p_now = [0,0,1]
                            s_now = [0,0,1]
                            e_now = [1,0,0]
                            after = [1,0,0]
                        else:
                            px = cw0-cw/4
                            p_now = [0,1,1]
                            s_now = [0,1,1]
                            e_now = [1,1,0]
                            aim = [1,0]
                            after = [1,1,0]
                    if rally == 1: #敵側のサーブ
                        pygame.draw.ellipse(screen,(255,0,0),(w*3/4-30,40,25,25))
                        if enemy_point %2 == 0:
                            p_now = [0,0,0]
                            s_now = [1,0,1]
                            e_now = [1,0,1]
                            after = [0,0,0]
                        else:
                            p_now = [0,1,0]
                            s_now = [1,1,1]
                            e_now = [1,1,1]
                            after = [0,1,0]
                    sub_aim  = [1,aim[0],aim[1]]
                    (px,py) = court_point(p_now,cw,ch,cs,cu,cw0,ch0)
                    (ex,ey) = court_point(e_now,cw,ch,cs,cu,cw0,ch0)
                    (sx,sy) = court_point(s_now,cw,ch,cs,cu,cw0,ch0)
                    (vx,vy) = movement(s_now,after,sv,cw,ch,cs,cu,cw0,ch0)
                    screen.blit(enemy, (ex-ew,ey-eh))
                    screen.blit(player, (px-pw,py-ph))
                    screen.blit(shuttle, (sx-sw,sy-sh))

                elif (mode == 2):
                    if rally == 0: #プレイヤー→敵
                        (sx,sy) = (sx+vx,sy+vy)
                        if e_stop == 0:
                            (ex,ey) = (ex+vex,ey+vey)
                            (ax,ay)  = court_point(after,cw,ch,cs,cu,cw0,ch0)  #目標の座標
                        if (ax-ev < ex  < ax+ev) and (ay-ev < ey < ay+ev):
                            e_now = after
                            (ex,ey) = court_point(after,cw,ch,cs,cu,cw0,ch0)
                            e_stop = 1
                        if (ax-sv < sx  < ax+sv) and (ay-sv < sy < ay+sv):  #シャトルストップ
                            s_now = after
                            (sx,sy)= court_point(s_now,cw,ch,cs,cu,cw0,ch0)
                            rally  = 3
                            wait = 0

                    elif rally == 1 or rally == 2: #敵→プレイヤー
                        if pressed_key[K_LEFT]:
                            aim[0] = 0
                        if pressed_key[K_RIGHT]:
                            aim[0] = 1
                        if pressed_key[K_UP]:
                            aim[1] -= 1
                            if aim[1] < 0:
                                aim[1] = 0
                        if pressed_key[K_DOWN]:
                            aim[1] += 1
                            if aim[1] > 2:
                                aim[1] = 2

                        else:
                            if rally == 1:
                                (sx,sy) = (sx+vx,sy+vy)
                                (ax,ay)  = court_point(after,cw,ch,cs,cu,cw0,ch0)
                                if (ax-sv < sx  < ax+sv) and (ay-sv < sy < ay+sv):
                                    s_now = after
                                    (sx,sy)= court_point(s_now,cw,ch,cs,cu,cw0,ch0)
                                    rally = 2  #プレイヤー打ち返し待ち
                                    wait = 0

                            elif rally == 2:
                                wait += 1
                                if wait > 10:
                                    enemy_point += 1
                                    mode = 1
                                    rally = 1
                                    aim = sub_aim
                    else:
                        wait += 1
                        if s_now == e_now:
                            rally = 1
                            after = [0,random.randint(0,1),random.randint(0,2)]
                            (vx,vy) = movement(s_now,after,sv,cw,ch,cs,cu,cw0,ch0)
                        if wait > 5:
                            player_point += 1
                            mode = 1
                            rally = 0

                    screen.blit(enemy, (ex-ew,ey-eh))
                    screen.blit(player, (px-pw,py-ph))
                    screen.blit(shuttle, (sx-sw,sy-sh))

        else:  #mode == 3  ゲーム終了
            if pressed_key[K_RETURN]:
                mode = 0
            else:
                screen.blit(enter_Surface, enter_Rect)
                screen.blit(gameset_Surface, gameset_Rect)
                result = pygame.font.Font('freesansbold.ttf', 200)
                result_Surface = result.render('{0} - {1}'.format(player_point, enemy_point), True, (255, 255, 255),(0,0,0))
                result_Rect = result_Surface.get_rect()
                result_Rect.center = (w/2,h/2)
                screen.blit(result_Surface, result_Rect)
                if player_point == game:
                    screen.blit(win_Surface, win_Rect)
                else:
                    screen.blit(lose_Surface, lose_Rect)



        for event in pygame.event.get():
            if mode == 1:
                if event.type == MOUSEBUTTONDOWN:
                    mode = 2

            elif mode == 2:
                if event.type == MOUSEMOTION:  #プレイヤー操作
                    px,py = event.pos
                    if px < cw0-cw/2:
                        px = cw0-cw/2
                    elif px > cw0+cw/2:
                        px = cw0+cw/2
                    if py < ch0:
                        py = ch0
                    elif py > ch0+ch/2:
                        py = ch0+ch/2

                if rally == 1 or  rally == 2:
                    if event.type == MOUSEBUTTONDOWN:
                        k_px, k_py = event.pos
                        p_now = inverse_court_point(k_px,k_py,cw,ch,cs,cu,cw0,ch0)
                        sub_s_now = inverse_court_point(sx,sy,cw,ch,cs,cu,cw0,ch0)
                        if p_now == sub_s_now:
                            sub_aim  = [1,aim[0],aim[1]]
                            after = sub_aim
                            s_now = sub_s_now
                            (sx,sy) = court_point(s_now,cw,ch,cs,cu,cw0,ch0)
                            (vx,vy) = movement(s_now,after,sv,cw,ch,cs,cu,cw0,ch0)
                            (vex,vey) = movement(e_now,after,ev,cw,ch,cs,cu,cw0,ch0)
                            e_stop = 0
                            rally = 0


            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

main()
