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

    #SCREEN.fill((0,0,0))
    pygame.display.update()

#全てのFishを表示する
def FishDisplay():
    for item in FishList:
        item.Display()

#終了判定
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
        #基本的なメンバー変数
        self.PosX = 0
        self.PosY = 0
        self.Angle = 0

        #画像に関するメンバー変数
        self.Pic = pic
        self.IsFacingRight = True

        #移動に関するメンバー変数
        self.SPEED = 5          #速度
        self.AMPLITUDE = 3      #振幅
        self.FREQUENCY= 5       #周波数
        self.FrequencyCount = 0 #Sin波のカウントアップ

        #その他メンバー関数に関するメンバー変数
        self.StartPos = [0,0]
        self.EndPos = [100,0]
        self.TanEaseCount = 0
        self.TanScale = 0

        #魚を表示させる
        SCREEN.blit(self.Pic, (self.PosX, self.PosY))


    #画面に表示する
    def Display(self):
        SCREEN.blit(self.Pic, (self.PosX, self.PosY))


    #前進
    def MoveForward(self):

        Between = round(math.sqrt((self.StartPos[0] - self.EndPos[0]) ** 2 + (self.StartPos[1] - self.EndPos[1]) ** 2), 2)
        NowBetween = round(math.sqrt((self.PosX - self.EndPos[0]) ** 2 + (self.PosY - self.EndPos[1]) ** 2), 2)


        if self.TanEaseCount == 0:
            self.TanEaseCount = 40

        #ここからNowBetweenが~って分岐をする
        if NowBetween < Between * 0.9:
            #End
            print("End")
            self.TanEaseCount += 1
            if 0 < self.TanScale:
                self.TanScale = math.fabs(1 - math.tan(math.radians(self.TanEaseCount)))
            else:
                self.TanScale = 0

        elif  Between * 0.1 < NowBetween:
            #Start
            print("Start")
            self.TanEaseCount += 1
            if self.TanScale < self.SPEED:
                self.TanScale = math.tan(math.radians(self.TanEaseCount))
            else:
                self.TanScale = 1
        
        else:
            #Between
            print("Between")
            self.TanEaseCount = 0
            self.TanScale = 1

        #直進
        self.PosX += math.cos(math.radians(self.Angle)) * self.SPEED
        self.PosY += math.sin(math.radians(self.Angle)) * self.SPEED

        #画像に対して垂直の角度を取得
        if self.IsFacingRight:
            VarticalAngle = self.Angle + 90 % 360
        else:
            VarticalAngle = self.Angle - 90

        #Sin波
        self.PosX += (math.sin(math.radians(self.FrequencyCount)) * math.cos(math.radians(VarticalAngle))) * self.AMPLITUDE
        self.PosY += (math.sin(math.radians(self.FrequencyCount)) * math.sin(math.radians(VarticalAngle))) * self.AMPLITUDE

        #カウントアップ
        self.FrequencyCount += self.FREQUENCY


########## 実行 ##########

#初期セットアップ
Setup()

while True:
    #画面のリセット
    SCREEN.fill((0,0,0))


    FishList[0].MoveForward()


    #表示する
    FishDisplay()

    #画面の更新とフレームレート制限
    pygame.display.update()
    clock.tick(24)

    #ループ抜け処理
    LoopOut()