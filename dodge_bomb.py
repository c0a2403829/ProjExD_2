import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA={
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0,5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect) ->tuple[bool,bool]:
    #横方向判定
    """
    引数:こうかとんRectまたは爆弾Rect
    戻り値:判定結果(横、縦)
    画面内ならTrue,画面外ならFalse
    """
    
    yoko, tate = True, True  # 横，縦方向用の変数
     # 横方向判定
    if rct.left < 0 or WIDTH < rct.right:  # 画面外だったら
        yoko = False
     # 縦方向判定
    if rct.top < 0 or HEIGHT < rct.bottom: # 画面外だったら
        tate = False
    return yoko, tate


def gameover(screen:pg.Surface)->None:
    """
    引数:screen
    戻り値:なし
    画面にgameoverを表示する
    """
    
    black_img = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(black_img,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
    black_img.set_alpha(125)

    fonto=pg.font.Font(None,80)
    txt=fonto.render("Game Over",
                     True,(255,255,255))
    
    crying_img = pg.image.load("fig/8.png")
    
    screen.blit(black_img,[0,0])
    screen.blit(txt,[400,250])
    screen.blit(crying_img,[330,250])
    screen.blit(crying_img,[730,250])
    pg.display.update()
    

def init_bb_imgs() ->tuple[list[pg.Surface], list[int]]:
    """
    引数:なし
    戻り値:２つのリストのタプル
    時間とともに爆弾が拡大，加速する
    """
    bb_accs=[a for a in range(1,11)]
    bb_imgs=[]
    for r in range(1,11):
        bb_img=pg.Surface((20*r,20*r))
        bb_imgs.append(bb_img)
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
        bb_img.set_colorkey((0,0,0))
    return bb_imgs,bb_accs


def get_kk_img(sum_mv:tuple[int,int])->pg.Surface:
    # for key,mv in DELTA.items():
    sum_mv==4

    
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")  
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    #爆弾初期化
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy= 5,5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        #ボールがこうかとんに当たったらgameoverしてgameを終わる
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            time.sleep(5)
            return 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0]+=mv[0] #左右
                sum_mv[1]+=mv[1] #上下
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        #徐々に早く、大きくする
        kk_rct.move_ip(sum_mv)
        bb_imgs,bb_accs=init_bb_imgs()
        avx=vx*bb_accs[min(tmr//500,9)]
        avy=vy*bb_accs[min(tmr//500,9)]
        bb_img=bb_imgs[min(tmr//500,9)]
        bb_rct.move_ip(avx,avy)
        screen.blit(bb_img,bb_rct)
        
        #画面外に出させない
        if check_bound(kk_rct)!= (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        yoko,tate=check_bound(bb_rct) 
        if not yoko:
            vx*=-1
        if not tate:
            vy*=-1
        
        screen.blit(kk_img, kk_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
