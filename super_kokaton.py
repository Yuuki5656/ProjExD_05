from asyncio import Event
import pygame as pg
import sys

WIDTH = 800
HEIGHT = 600

class Bird(pg.sprite.Sprite):
    """
    ゲームキャラクター(こうかとん)に関するクラス
    """
    def __init__(self,num: int,x: int):
        """
        こうかとん画像Surfaceを生成する
        引数1 num:こうかとん画像ファイル名の番号
        """
        super().__init__()
        self.mode = 0
        self.jump = 0
        self.cnt = 0
        self.img = pg.image.load(f"ex05/fig/{num}.png")
        self.rect = self.img.get_rect()
        self.rect.centerx = x
        self.rect.centery = 450
    def update(self,screen: pg.Surface):
        """
        
        """
        if self.mode == 0:
            screen.blit(self.img,self.rect)
        if self.mode == 1:
            screen.blit(pg.transform.flip(self.img,True,False),self.rect)
        if self.jump == 1:
            self.rect.centery -=5
            if self.rect.centery <= 300:
                self.cnt +=1
                self.rect.centery += 5
                if self.cnt >=20:
                    self.jump = 0
                    self.cnt = 0
        if self.jump == 0 and self.rect.centery < 450:
            self.rect.centery += 5

class Background:
    """
    背景の処理をする
    """
    def __init__(self,screen:pg.Surface):
        self.x=0
        self.bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
        self.bg_img_fl = pg.transform.flip(self.bg_img,True,False)
        screen.blit(self.bg_img_fl,[-800,0])
    def update(self,screen:pg.Surface):
        """
        移動に応じたupdateを行う
        """
        self.x%=3200
        screen.blit(self.bg_img,[800-self.x,0])
        screen.blit(self.bg_img_fl,[2400-self.x,0])
        screen.blit(self.bg_img_fl,[-800-self.x,0])


class Enemy(pg.sprite.Sprite):
    """"
     敵に関するクラス
    """
    def __init__(self, screen: pg.Surface, e_x: int, bg: Background):
        super().__init__()
        self.e_x=e_x
        self.ene_img = pg.transform.rotozoom(pg.image.load("ex05/fig/monster11.png"),0,0.2)
        self.rect= self.ene_img.get_rect()
        self.rect.centerx = self.e_x - bg.x
        self.rect.centery = 450
        screen.blit(self.ene_img,self.rect)

    def update(self, screen: pg.Surface):
        self.rect.centerx -= 5
        screen.blit(self.ene_img,self.rect)


class Goal(pg.sprite.Sprite):
    """"
     ゴール
    """
    def __init__(self, screen: pg.Surface):
        super().__init__()
        self.g_img = pg.transform.rotozoom(pg.image.load("ex05/fig/torinosu_egg.png"),0,0.2)
        self.rect = self.g_img.get_rect()
        self.rect.centerx = 3200
        self.rect.centery = 450
        screen.blit(self.g_img,self.rect)

    def update(self, screen: pg.Surface,bg: Background):
        self.rect.centerx = 3200 - bg.x
        screen.blit(self.g_img,self.rect)

class Score:
    """
    残り時間や敵の数をスコアとして表示するクラス
    """
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (0, 0, 255)
        self.score = 0
        self.image = self.font.render(f"Score: {self.score}", 0, self.color)
        self.rect = self.image.get_rect()
        self.whi = 700
        self.hei = 500
        self.rectcenter = self.whi, self.hei
    
    def score_up(self, add):
        self.score += add

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"Score: {self.score}", 0, self.color)
        screen.blit(self.image, self.rect)


def main():
    pg.display.set_caption("Super_Kokaton")
    screen = pg.display.set_mode((WIDTH,HEIGHT))

    bird = Bird(2,200)
    bg = Background(screen)
    enes = pg.sprite.Group()
    gls = pg.sprite.Group()
    for i in range(3):
        enes.add(Enemy(screen,i*400+800,bg))
    gl = Goal(screen)
    gls.add(gl)

    tmr = 0
    clock = pg.time.Clock()

    score = Score()
    
    while True:
        for  event in pg.event.get():
            if event.type == pg.QUIT: return
        if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
            bird.mode = 0
            bg.x += 10
        if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
            bird.mode = 1
            bg.x -= 10
        if bg.x <= 0:
            bg.x = 0
        if bird.rect.centerx >= gl.rect.centerx:
            bg.x = 3000
            score.score_up(3000)
        if bird.rect.centery == 450 and event.type == pg.KEYDOWN and event.key == pg.K_UP:
            bird.jump=1
        for ene in pg.sprite.spritecollide(bird, enes, True):
            return
        for goal in pg.sprite.spritecollide(bird,gls,False):
            return 

        tmr += 1
        x = tmr%3200

        bg.update(screen)
        bird.update(screen)
        enes.update(screen)
        gls.update(screen,bg)
        score.update(screen)
        pg.display.update()
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

