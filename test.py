import sys, random, math, os, cv2
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
BEZEL = 50
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
        self.Angle = 180

        #画像に関するメンバー変数
        self.Pic = pic
        self.IsFacingRight = True

        #移動に関するメンバー変数
        self.SPEED = 5          #速度
        self.AMPLITUDE = 3      #振幅
        self.FREQUENCY= 5       #周波数

        #その他メンバー関数に関するメンバー変数
        self.SF_SinEaseCount = 0    
        self.SF_FrequencyCount = 0  #Sin波のカウントアップ
        self.SF_RemainingValue = 0  #残り移動量
        self.SF_IsFirstTime = True  #初回かどうか

        self.QF_RemainingValue = 0
        self.QF_IsFirstTime = True

        self.SA_RemainingValue = 0
        self.SA_IsFirstTime = True

        self.QA_RemainingValue = 0
        self.QA_IsFirstTime = True

        self.PR_MainProcessNum = 2
        self.PR_SubProcessNum = 0
        self.PR_SubProcessLimit = 0
        self.PR_IsMainProcessStart = True
        self.PR_IsSubProcessStart = True
        self.PR_MainRepeatCount = 0
        self.PR_SubRepeatCount = 0
        self.PR_Value = 0

        #魚を表示させる
        Screen.blit(self.Pic, (self.PosX, self.PosY))


    #画面に表示する
    def Display(self):
        #画面端移動
        if ScreenWidth + BEZEL < self.PosX:
            #print("右端")
            self.PosX = -BEZEL
        elif self.PosX < 0 - BEZEL:
            self.PosX = ScreenWidth + BEZEL
            #print("左端")
        
        if ScreenHeight + BEZEL < self.PosY:
            self.PosY = -BEZEL
            #print("下端")
        elif self.PosY < 0 - BEZEL:
            self.PosY = ScreenHeight + BEZEL
            #print("上端")

        #Angleの調節
        self.Angle = self.Angle % 360

        #画像の反転
        pic = self.Pic
        if 90 < self.Angle and self.Angle < 270:
            ArrayPic = pygame.surfarray.array3d(pic)
            ArrayPic = cv2.flip(ArrayPic, 1)
            pic = pygame.surfarray.make_surface(ArrayPic)

        #画像の回転
        pic = pygame.transform.rotate(pic, self.Angle * -1)
        ImageRect = self.Pic.get_rect()
        CenterX = ImageRect.width // 2
        CenterY = ImageRect.height // 2
        RotatedRect = pic.get_rect(center=(self.PosX + CenterX, self.PosY + CenterY))

        Screen.blit(pic, RotatedRect.topleft)


    #前進
    def SlowMoveForward(self, distance, speed = -1):

        #一回きりの処理
        if self.SF_IsFirstTime:
            self.SF_SinEaseCount = 0
            self.SF_RemainingValue = distance
            self.SF_IsFirstTime = False

        DBScene = "null"
        SinIncVal = 90 / (FLAMELATE * 2)
        if speed == -1:
            speed = self.SPEED
        
        #速度に掛ける"SinIncVal"の設定とアーリーリターン
        if distance * 0.9 < self.SF_RemainingValue:
            #Start
            self.SF_SinEaseCount += SinIncVal
            if self.SF_SinEaseCount <= 90:
                SinScale = round(math.sin(math.radians(self.SF_SinEaseCount)), 2)
            else:
                SinScale = 1

        elif self.SF_RemainingValue < distance * 0.1:
            #End
            self.SF_SinEaseCount += SinIncVal
            if self.SF_SinEaseCount <= 180:
                SinScale = round(math.sin(math.radians(self.SF_SinEaseCount)), 2)
            #アーリーリターン
            else:
                self.SF_IsFirstTime = True
                return True

        else:
            #Between
            self.SF_SinEaseCount = 90
            SinScale = 1
        

        #print("DBScene = " + DBScene + " | SinScale = " + str(SinScale) + " | SF_SinEaseCount = " + str(self.SF_SinEaseCount) + " | NowDistance = " + str(self.SF_RemainingValue) + " | Distance = " + str(distance))

        #移動先の座標を決定する
        #直進
        XIncreace = math.cos(math.radians(self.Angle)) * speed * SinScale
        YIncreace = math.sin(math.radians(self.Angle)) * speed * SinScale
        self.PosX += XIncreace
        self.PosY += YIncreace

        #SF_RemainingValueの更新
        self.SF_RemainingValue -= round(math.sqrt(XIncreace ** 2 + YIncreace ** 2), 2)
        
        #画像に対して垂直の角度を取得
        if self.IsFacingRight:
            VarticalAngle = self.Angle + 90 % 360
        else:
            VarticalAngle = self.Angle - 90

        #Sin波
        self.PosX += (math.sin(math.radians(self.SF_FrequencyCount)) * math.cos(math.radians(VarticalAngle))) * self.AMPLITUDE * SinScale
        self.PosY += (math.sin(math.radians(self.SF_FrequencyCount)) * math.sin(math.radians(VarticalAngle))) * self.AMPLITUDE * SinScale

        #カウントアップ
        self.SF_FrequencyCount += self.FREQUENCY

        return False


    def QuickMoveForward(self, distance):
        if self.QF_IsFirstTime:
            self.QF_RemainingValue = distance
            self.QF_IsFirstTime = False

        #Endアーリーリターン
        if self.QF_RemainingValue < 1:
            self.QF_RemainingValue = 0
            self.QF_IsFirstTime = True
            return True
        
        #Move
        IncreaceValue = self.QF_RemainingValue / 5.5
        self.PosX += IncreaceValue * math.cos(math.radians(self.Angle))
        self.PosY += IncreaceValue * math.sin(math.radians(self.Angle))
        self.QF_RemainingValue -= IncreaceValue
        
        return False

    def QuickAngleChange(self, angle):
        if self.QA_IsFirstTime:
            self.QA_RemainingValue = angle
            self.QA_IsFirstTime = False

        if abs(self.QA_RemainingValue) < 1:
            self.QA_RemainingValue = 0
            self.QA_IsFirstTime = True
            return True
        
        IncreaceValue = self.QA_RemainingValue / 4
        self.Angle += IncreaceValue
        self.QA_RemainingValue -= IncreaceValue
        
        return False
        

    def SlowAngleChange(self, angle):
        if self.SA_IsFirstTime:
            self.SA_RemainingValue = angle
            self.SA_IsFirstTime = False

        if abs(self.SA_RemainingValue) < 3:
            self.SA_RemainingValue = 0
            self.SA_IsFirstTime = True
            return True
        
        IncreaceValue = angle / abs(angle) * 2
        self.Angle += IncreaceValue
        self.SA_RemainingValue -= IncreaceValue
        print(self.SA_RemainingValue)

        #直進
        XIncreace = math.cos(math.radians(self.Angle)) * self.SPEED
        YIncreace = math.sin(math.radians(self.Angle)) * self.SPEED
        self.PosX += XIncreace
        self.PosY += YIncreace
        
        return False
    
    def Process(self):

        def SubReset():
            self.PR_IsSubProcessStart = True
            self.PR_SubRepeatCount = 0
            self.PR_Value = 0

        def MainReset():
            SubReset()
            self.PR_MainProcessNum = random.randrange(0, 4)
            self.PR_SubProcessNum = 0
            self.PR_SubProcessLimit = 0
            self.PR_IsMainProcessStart = True
            self.PR_MainRepeatCount = 0

        def SubStart(val1, val2):
            if self.PR_IsSubProcessStart:
                self.PR_SubRepeatCount = random.randrange(val1, val2)
                self.PR_Value = self.PR_SubRepeatCount
                self.PR_IsSubProcessStart = False

        #ループさせない場合は、val1を-1,val2を0にするなどして"PR_TargetMainRepeatCount"を0未満にする
        def MainStart(limit, val1, val2):
            if self.PR_IsMainProcessStart:
                self.PR_MainRepeatCount = random.randrange(val1, val2)
                self.PR_SubProcessLimit = limit
                self.PR_IsMainProcessStart = False
                print("MainStart")

        def ProcessChange(isEnd, targetStatus = -1, chance = -1):
            if isEnd:

                #確率で指定ステータスへ遷移
                if targetStatus != -1 and chance != -1:
                    if random.randrange(0, 101) < chance:
                        #遷移成功
                        self.PR_SubProcessNum = targetStatus
                        SubReset()
                        return
                    else:
                        #遷移失敗
                        print()

                #最終ステータスかどうか
                if self.PR_SubProcessNum != self.PR_SubProcessLimit:
                    #最終ではない
                    self.PR_SubProcessNum += 1
                    SubReset()
                    print("subreset")
                    return
                else:
                    #最終
                    #ループが残っているかどうか
                    if self.PR_MainRepeatCount < 0:
                        #ループが残っていない
                        MainReset()
                        print("mainend")
                        return
                    else:
                        #ループが残っている
                        SubReset()
                        self.PR_SubProcessNum = 0
                        self.PR_MainRepeatCount -= 1
                        print("mainloop")
                        return

        #MainProcess-0
        if self.PR_MainProcessNum == 0:
            MainStart(3, 3, 10)

            if self.PR_SubProcessNum == 0:
                SubStart(1, 40)
                self.PR_SubRepeatCount -= 1
                ProcessChange(self.PR_SubRepeatCount < 0)
                print("0-0")
                return
            
            elif self.PR_SubProcessNum == 1:
                SubStart(-120, 120)
                IsSubProcessEnd = self.QuickAngleChange(self.PR_Value)
                ProcessChange(IsSubProcessEnd)
                print("0-1")
                return
                
            elif self.PR_SubProcessNum == 2:
                SubStart(1, 12)
                self.PR_SubRepeatCount -= 1
                ProcessChange(self.PR_SubRepeatCount < 0)
                print("0-2")
                return
            
            elif self.PR_SubProcessNum == 3:
                SubStart(100, 200)
                IsSubProcessEnd = self.QuickMoveForward(self.PR_Value)
                ProcessChange(IsSubProcessEnd, 2, 30)
                print("0-3")
                return
        
        #MainProcess-1
        elif self.PR_MainProcessNum == 1:
            MainStart(1, -1, 0)

            if self.PR_SubProcessNum == 0:
                SubStart(1, 40)
                self.PR_SubRepeatCount -= 1
                ProcessChange(self.PR_SubRepeatCount < 0)
                print("1-0")
                return
            
            elif self.PR_SubProcessNum == 1:
                SubStart(200, 1200)
                IsSubProcessEnd = self.QuickMoveForward(self.PR_Value)
                ProcessChange(IsSubProcessEnd)
                print("1-1")
                return
            
        #Process-2
        elif self.PR_MainProcessNum == 2:
            MainStart(1, 3, 10)

            if self.PR_SubProcessNum == 0:
                SubStart(-300, 300)
                IsSubProcessEnd = self.SlowAngleChange(self.PR_Value)
                ProcessChange(IsSubProcessEnd)
                #print("2-0")
                return

            elif self.PR_SubProcessNum == 1:
                SubStart(100, 1000)
                IsSubProcessEnd = self.SlowMoveForward(self.PR_Value)
                ProcessChange(IsSubProcessEnd)
                print("2-1")
                return
        
        #Process-3
        elif self.PR_MainProcessNum == 3:
            MainStart(0, -1, 0)

            if self.PR_SubProcessNum == 0:
                SubStart(10, 40)
                IsSubProcessEnd = self.SlowMoveForward(self.PR_Value, 1)
                ProcessChange(IsSubProcessEnd)
                print("3-0")
                return


########## 実行 ##########

#初期セットアップ
Setup()
while True:
    #画面のリセット
    Screen.fill((0,0,0))


    FishList[0].Process()


    #表示する
    FishDisplay()

    #画面の更新とフレームレート制限
    pygame.display.update()
    clock.tick(FLAMELATE)

    #ループ抜け処理
    LoopOut()