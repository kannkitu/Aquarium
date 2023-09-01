import sys, random, math, os
import pygame, pygame.locals

#Pygameの初期化
pygame.init()

########## 変数群 ##########

#スクリーン
Screen = pygame.display.set_mode((1280, 720))
#スクリーンサイズ
ScreenWidth = Screen.get_width()
ScreenHeight = Screen.get_height()
#ベゼル
BEZEL = 200
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

    #Screen.fill((0,0,0))
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
        self.PosX = 100
        self.PosY = 100
        self.Angle = 30

        #画像に関するメンバー変数
        self.Pic = pic
        self.IsFacingRight = True

        #移動に関するメンバー変数
        self.SPEED = 5          #速度
        self.AMPLITUDE = 3      #振幅
        self.FREQUENCY= 5       #周波数

        #その他メンバー関数に関するメンバー変数
        self.MF_SinEaseCount = 0    
        self.MF_FrequencyCount = 0  #Sin波のカウントアップ
        self.MF_RemainingValue = 0  #残り移動量
        self.MF_IsFirstTime = True  #初回かどうか

        self.QF_RemainingValue = 0
        self.QF_IsFirstTime = True

        self.SA_RemainingValue = 0
        self.SA_IsFirstTime = True

        self.QA_RemainingValue = 0
        self.QA_IsFirstTime = True

        #デバッグ用
        self.DB_Scene = ""

        #魚を表示させる
        Screen.blit(self.Pic, (self.PosX, self.PosY))


    #画面に表示する
    def Display(self):
        #画面端移動
        if ScreenWidth + BEZEL < self.PosX:
            self.PosX = -BEZEL
        elif self.PosX < 0 - BEZEL:
            self.PosX = ScreenWidth + BEZEL
        
        if ScreenHeight + BEZEL < self.PosY:
            self.PosY = -BEZEL
        elif self.PosY < 0 - BEZEL:
            self.PosX = ScreenHeight + BEZEL

        #画像の回転
        pic = pygame.transform.rotate(self.Pic, self.Angle * -1)
        ImageRect = self.Pic.get_rect()
        CenterX = ImageRect.width // 2
        CenterY = ImageRect.height // 2
        RotatedRect = pic.get_rect(center=(self.PosX + CenterX, self.PosY + CenterY))

        Screen.blit(pic, RotatedRect.topleft)


    #前進
    def MoveForward(self, distance):

        #一回きりの処理
        if self.MF_IsFirstTime:
            self.MF_SinEaseCount = 0
            self.MF_RemainingValue = distance
            self.MF_IsFirstTime = False

        DBScene = "null"
        SinIncVal = 90 / (FLAMELATE * 2)
        
        #速度に掛ける"SinIncVal"の設定とアーリーリターン
        if distance * 0.9 < self.MF_RemainingValue:
            #Start
            self.DB_Scene = "MoveForward_Start"

            self.MF_SinEaseCount += SinIncVal
            if self.MF_SinEaseCount <= 90:
                SinScale = round(math.sin(math.radians(self.MF_SinEaseCount)), 2)
            else:
                SinScale = 1

        elif self.MF_RemainingValue < distance * 0.1:
            #End
            self.DB_Scene = "MoveForward_End"

            self.MF_SinEaseCount += SinIncVal
            if self.MF_SinEaseCount <= 180:
                SinScale = round(math.sin(math.radians(self.MF_SinEaseCount)), 2)
            #アーリーリターン
            else:
                self.MF_IsFirstTime = True
                return False

        else:
            #Between
            self.DB_Scene = "MoveForward_Normal"

            self.MF_SinEaseCount = 90
            SinScale = 1
        

        print("DBScene = " + DBScene + " | SinScale = " + str(SinScale) + " | MF_SinEaseCount = " + str(self.MF_SinEaseCount) + " | NowDistance" + str(self.MF_RemainingValue) + " | Distance" + str(distance))

        #移動先の座標を決定する
        #直進
        XIncreace = math.cos(math.radians(self.Angle)) * self.SPEED * SinScale
        YIncreace = math.sin(math.radians(self.Angle)) * self.SPEED * SinScale
        self.PosX += XIncreace
        self.PosY += YIncreace

        #MF_RemainingValueの更新
        self.MF_RemainingValue -= round(math.sqrt(XIncreace ** 2 + YIncreace ** 2), 2)
        
        #画像に対して垂直の角度を取得
        if self.IsFacingRight:
            VarticalAngle = self.Angle + 90 % 360
        else:
            VarticalAngle = self.Angle - 90

        #Sin波
        self.PosX += (math.sin(math.radians(self.MF_FrequencyCount)) * math.cos(math.radians(VarticalAngle))) * self.AMPLITUDE * SinScale
        self.PosY += (math.sin(math.radians(self.MF_FrequencyCount)) * math.sin(math.radians(VarticalAngle))) * self.AMPLITUDE * SinScale

        #カウントアップ
        self.MF_FrequencyCount += self.FREQUENCY

        return True


    def QuickMoveForward(self, distance):

        if self.QF_IsFirstTime:
            self.QF_RemainingValue = distance
            self.QF_IsFirstTime = False

        #Endアーリーリターン
        if self.QF_RemainingValue < 1:
            return False
        
        #Move
        IncreaceValue = self.QF_RemainingValue / 5.5
        self.PosX += IncreaceValue * math.cos(math.radians(self.Angle))
        self.PosY += IncreaceValue * math.sin(math.radians(self.Angle))
        self.QF_RemainingValue -= IncreaceValue
        
        return True

    def QuickAngleChange(self, angle):

        if self.QA_IsFirstTime:
            self.QA_RemainingValue = angle
            self.QA_IsFirstTime = False

        if abs(self.QA_RemainingValue) < 1:
            self.QA_RemainingValue = 0
            self.QA_IsFirstTime = True
            return False
        
        IncreaceValue = self.QA_RemainingValue / 4
        self.Angle += IncreaceValue
        self.QA_RemainingValue -= IncreaceValue

        print(self.QA_RemainingValue)
        
        return True
        

    def SlowAngleChange(self, angle):

        if self.SA_IsFirstTime:
            self.SA_RemainingValue = angle
            self.SA_IsFirstTime = False

        if abs(self.SA_RemainingValue) < 1:
            self.SA_RemainingValue = 0
            self.SA_IsFirstTime = True
            return False
        
        IncreaceValue = angle / abs(angle) * 2
        self.Angle += IncreaceValue
        self.SA_RemainingValue -= IncreaceValue

        #直進
        XIncreace = math.cos(math.radians(self.Angle)) * self.SPEED
        YIncreace = math.sin(math.radians(self.Angle)) * self.SPEED
        self.PosX += XIncreace
        self.PosY += YIncreace
        
        return True


########## 実行 ##########

#初期セットアップ
Setup()

while True:
    #画面のリセット
    Screen.fill((0,0,0))


    FishList[0].MoveForward(2000)


    #表示する
    FishDisplay()

    #画面の更新とフレームレート制限
    pygame.display.update()
    clock.tick(FLAMELATE)

    #ループ抜け処理
    LoopOut()