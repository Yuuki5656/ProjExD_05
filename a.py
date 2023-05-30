import pygame as pg
import sys




class Bird(pg.sprite.Sprite):
    """
    プレイヤーに関するクラス
    """
    delta = { #とりあえず左右移動とジャンプだけ
        pg.K_LEFT: (-1,0),
        pg.K_RIGHT: (1,0),
        pg.K_UP: (0,-1)
    }


    def __init__(self, num: int, xy: tuple[int, int]):
        """
        プレイヤー画像Surfaceを生成する
        引数1 num:プレイヤー画像ファイル名の番号
        引数2 xy:プレイヤー画像の位置座標タプル
        """
        super().__init__()
        img = pg.transform.rotozoom(pg.image.load(f"ex05/fig/{num}.png"), 0, 1.0)
        self.imgs = {
            0: img,
            1: pg.transform.flip(img,True,False),
        }
        self.mode = 0 # 右向き(初期状態)
        self.img = self.imgs[self.mode]
        self.rect = self.img.get_rect()
        self.rect.center = xy

    def update(self, key_lst: list[bool],screen: pg.Surface):
        """
        押下キーにおうじてプレイヤーの向きを変える
        """
        
        screen.blit(self.img, self.rect)

class Background():
    def __init__(self, screen):
        self.screen = screen
        self.tmr = 0
        self.x = self.tmr%3200

class Sucore:
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
    pg.display.set_caption("未定")
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    bg_img2 = pg.transform.flip(bg_img, True, False)

    bird = Bird(2, (250, 450))

    enemy_img = pg.image.load("ex05/fig/monster11.png")

    tmr = 0

    while True:
        key_lst = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        tmr += 1
        x = tmr%3200
        screen.blit(bg_img, [-x, 0])
        screen.blit(bg_img2, [1600-x, 0])
        screen.blit(bg_img, [3200-x, 0])

        bird.update(screen)
        pg.display.update()
        clock.tick(100)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

