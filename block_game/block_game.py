import pygame
from pygame.locals import *
import sys
import random

def reset(a,b,x,y,screen,l,r):
    screen.fill((0,0,0,0))
    player = pygame.draw.line(screen,(200,200,200), (a-l/2,b), (a+l/2,b), 10)
    player.center = (a,b)
    ball = pygame.draw.ellipse(screen, (100,200,200), (x-r,y-r,r,r))
    ball.center = (x,y)

def block_long(w,max,min,n,aida):  #max,min=ブロックの長さの最大、最小 n=段数、　aida = ブロック間の距離
    block = []
    for i in range(0,n):
        i_block = []
        rm = w - 2 * aida  #残りの隙間
        while (rm >= max):
            long = random.randint(min,max)
            i_block.append(long)
            rm -= (long + aida)
        i_block.append(rm)
        block.append(i_block)
    return  block


def make_block(block,screen,n,hutosa,aida,judge): #hutosa = ブロックの厚さ
    for i in range(0,n):
        i_block = block[i]
        hasi = aida
        for k in range(0,len(i_block)):
            l = i_block[k]  #ブロックの長さ
            if judge[i][k] == 0:
                (ia, ib) = (hasi+l/2, aida * (i + 2) + hutosa * (i + 1))
                pygame.draw.line(screen, (50,50,200), (ia-l/2,ib), (ia+l/2, ib), hutosa)
            hasi += (l + aida)

def make_judge(block):
    judge = []
    for i in range(0,len(block)):
        n = len(block[i])
        i_judge  = [0]*n
        judge.append(i_judge)
    return judge

def main():
    pygame.init()
    (w,h) = (1000, 600)
    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption('Block Crush Game')

    (a,b) = (w/2, h-50)  #棒の位置
    l = 100  #棒の長さ

    (x0,y0) = (w/2, h-300) #ボールの位置
    (x,y) = (x0,y0)
    r = 30 #ボールの半径
    (vx0, vy0) = (2, 1)
    (vx, vy) = (vx0, vy0)

    hutosa = 30
    n = 5
    aida = 5
    max = 400
    min = 100
    block = block_long(w,max,min,n,aida)
    judge = make_judge(block)

    start = pygame.font.Font('freesansbold.ttf', 200)
    start_Surface = start.render('START', True, (200, 200, 100),(0,0,0))
    start_Rect = start_Surface.get_rect()
    start_Rect.center = (w/2,150)

    end  = pygame.font.Font('freesansbold.ttf', 100)
    end_Surface = end.render('GAME OVER', True, (100, 200, 100), (0, 0, 0))
    end_Rect = end_Surface.get_rect()
    end_Rect.center = (w/2,h/2)

    clear  = pygame.font.Font('freesansbold.ttf', 100)
    clear_Surface = clear.render('CLEAR!!!', True, (200, 100, 100), (0, 0, 0))
    clear_Rect = clear_Surface.get_rect()
    clear_Rect.center = (w/2,h/2)

    enter  = pygame.font.Font('freesansbold.ttf', 50)
    enter_Surface = enter.render('Press enter key.', True, (200, 200, 200), (0, 0, 0))
    enter_Rect = enter_Surface.get_rect()
    enter_Rect.center = (w/2,h*3/4)

    mode = 0

    while True:
        pygame.display.update()
        pygame.time.wait(1)

        j = 0
        for i in range(0,n):
            if j == 0:
                if judge[i] != [1] * len(judge[i]):
                    j = 1
        if j == 0:
            mode = 3


        if mode == 1:
            reset(a,b,x,y,screen,l,r)
            make_block(block,screen,n,hutosa,aida,judge)
            xb = x + vx
            yb = y + vy

            if (a-l/2-r < xb < a+l/2+r) and (b-r < yb < b+r):  #プレイヤーの動かす棒との接触
                vy = vy * (-1)
                if (a-l/2-vx < xb < a-l/2) or (a+l/2 < xb < a+l/2+vx):
                    vx = vx * (-1)

            j_mode = 0
            for i in range(0,n):
                if j_mode == 1:
                    break
                else:
                    j  = n-i-1
                    j_block = block[j]  #下の段から順番に判断
                    edge = aida
                    for k in range(0,len(j_block)):
                        if j_mode == 1:
                            break
                        elif judge[j][k] == 0:  #まだ壊されていないブロックか
                            if (edge-r < xb < edge + j_block[k]+r) and (yb < (hutosa + aida)*j + hutosa+r):
                                j_mode =  1
                                judge[j][k] = 1  #ぶつかった
                                vy = vy * (-1)
                                y = y+hutosa
                                if (edge-r < xb < edge) or (edge + j_block[k] < vx < edge + j_block[k]+r):
                                    vx = vx * (-1)
                        edge += (j_block[k] + aida)


            if (r <= xb <= w-r):  #x軸壁方向との接触
                x = xb
            else:
                vx = vx * (-1)

            if (0 <= yb <= h):  #y軸壁方向との接触
                y = yb
            elif yb < r :
                vy = vy * (-1)
            else:
                mode = 2

        elif mode == 0:  #始まり
            reset(a,b,x,y,screen,l,r)
            screen.blit(start_Surface, start_Rect)
            screen.blit(enter_Surface, enter_Rect)

        elif mode == 2: #終わり(game over)
            screen.fill((0,0,0,0))
            screen.blit(end_Surface, end_Rect)
            screen.blit(enter_Surface, enter_Rect)

        elif  mode == 3:  #クリア
            screen.fill((0,0,0,0))
            screen.blit(clear_Surface, clear_Rect)
            screen.blit(enter_Surface, enter_Rect)


        for event in pygame.event.get():
            pressed_key = pygame.key.get_pressed()
            if mode == 1:
                if event.type == MOUSEMOTION:  #棒をマウスの位置によって動かす
                    ap, bp = event.pos
                    if (l/2 <= ap <=  w-l/2):
                        a  = ap
                    elif ap < l/2:
                        a  = l/2
                    else:
                        a = w-l/2

            elif mode == 0:
                if pressed_key[K_RETURN]:
                    mode = 1

            else:
                if pressed_key[K_RETURN]:
                    block = block_long(w,max,min,n,aida)
                    judge = make_judge(block)
                    (a,b) = (w/2, h-50)
                    (x,y) = (x0, y0)
                    (vx, vy) = (vx0, vy0)
                    mode = 0

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

main()
