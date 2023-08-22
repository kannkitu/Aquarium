import sys, random, math, os
import pygame, pygame.locals

#Pygameの初期化
pygame.init()

########## 変数群 ##########

#スクリーン
SCREEN = pygame.display.set_mode((1280, 720))
#初期の魚の数
FISHNUM = 7
#クラスFishが入る
FishList = []
#フレームレート制限用
clock = pygame.time.Clock()


########## 関数群 ##########

#初期セットアップを行う関数
def Setup():
    #初期の魚を読み込む処理
    for i in range(FISHNUM):
        FileName = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resource", str(i) + ".png")
        Image = pygame.image.load(FileName)
        FishList.append(Fish(Image))

    pygame.display.update()


def LoopOut():
    #ループ抜け処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


########## クラス ##########

class Fish:

    #コンストラクタ
    def __init__(self, pic):
        #メンバー変数(表示関連)の初期化
        self.PosX = 0
        self.PosY = 0

        self.Angle = 0
        self.VarticalAngle = 90
        self.IsFacingRight = True

        self.Speed = 10
        self.Amplitude = 5  #振幅
        self.Frequency = 10 #周波数
        self.FrequencyCount = 0

        self.Pic = pic

        #メンバー変数(移動関連)の初期化
        self.MoveCount = 0

        #魚を表示させる
        SCREEN.blit(self.Pic, (self.PosX, self.PosY))

    #前進
    def MoveForward(self):
        #直進
        self.PosX += math.cos(math.radians(self.Angle)) * self.Speed
        self.PosY += math.sin(math.radians(self.Angle)) * self.Speed

        print(self.PosX)
        print(self.PosY)

        #画像に対して垂直の角度を取得
        if self.IsFacingRight:
            self.VarticalAngle = self.Angle + 90 % 360
        else:
            self.VarticalAngle = self.Angle - 90

        #Sin波
        self.PosX += (math.sin(math.radians(self.FrequencyCount)) * math.cos(math.radians(self.VarticalAngle))) * self.Amplitude
        self.PosY += (math.sin(math.radians(self.FrequencyCount)) * math.sin(math.radians(self.VarticalAngle))) * self.Amplitude

        #
        SCREEN.blit(self.Pic, (self.PosX, self.PosY))

        #カウントアップ
        self.FrequencyCount += self.Frequency

########## 実行 ##########

#初期セットアップ
Setup()

while True:
    LoopOut()
    FishList[0].MoveForward()
    pygame.display.update()
    clock.tick(24)