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
FLAMELATE = 24


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
    FishList[0].Display()
    #for item in FishList:
        #item.Display()

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
        self.SinEaseCount = 0
        self.SinIncVal = 1
        self.SinScale = 0
        self.MaxSinScale = 0

        self.MF_NowDistance = 0

        #魚を表示させる
        SCREEN.blit(self.Pic, (self.PosX, self.PosY))


    #画面に表示する
    def Display(self):
        SCREEN.blit(self.Pic, (self.PosX, self.PosY))

    
    #前進
    def MoveForward(self, distance):

        DBScene = "null"
        SinIncVal = 90 / (FLAMELATE * 2)

        
        if self.SinEaseCount == 0:
            self.MF_NowDistance = distance

        #速度に掛ける"SinIncVal"を設定
        if distance * 0.9 < self.MF_NowDistance:
            #Start
            DBScene = "Start"
            self.SinEaseCount += SinIncVal
            if self.SinEaseCount <= 90:
                self.SinScale = round(math.sin(math.radians(self.SinEaseCount)), 2)
        elif self.MF_NowDistance < distance * 0.1:
            #End
            DBScene = "End"
            self.SinEaseCount += SinIncVal
            if self.SinEaseCount <= 180:
                self.SinScale = round(math.sin(math.radians(self.SinEaseCount)), 2)
        else:
            #Between
            DBScene = "Between"
            self.SinEaseCount = 90
            self.SinScale = 1

        print("DBScene = " + DBScene + " | SinScale = " + str(self.SinScale) + " | SinEaseCount = " + str(self.SinEaseCount) + " | NowDistance" + str(self.MF_NowDistance) + " | Distance" + str(distance))

        #移動先の座標を決定する
        #直進
        XIncreace = math.cos(math.radians(self.Angle)) * self.SPEED * self.SinScale
        YIncreace = math.sin(math.radians(self.Angle)) * self.SPEED * self.SinScale
        self.PosX += XIncreace
        self.PosY += YIncreace

        #NowDistanceの更新
        self.MF_NowDistance = self.MF_NowDistance - math.sqrt(XIncreace ** 2 + YIncreace ** 2)
        
        #画像に対して垂直の角度を取得
        if self.IsFacingRight:
            VarticalAngle = self.Angle + 90 % 360
        else:
            VarticalAngle = self.Angle - 90

        #Sin波
        self.PosX += (math.sin(math.radians(self.FrequencyCount)) * math.cos(math.radians(VarticalAngle))) * self.AMPLITUDE * self.SinScale
        self.PosY += (math.sin(math.radians(self.FrequencyCount)) * math.sin(math.radians(VarticalAngle))) * self.AMPLITUDE * self.SinScale

        #カウントアップ
        self.FrequencyCount += self.FREQUENCY



########## 実行 ##########

#初期セットアップ
Setup()

while True:
    #画面のリセット
    SCREEN.fill((0,0,0))


    FishList[0].MoveForward(300)


    #表示する
    FishDisplay()

    #画面の更新とフレームレート制限
    pygame.display.update()
    clock.tick(FLAMELATE)

    #ループ抜け処理
    LoopOut()