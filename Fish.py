import random, math, os, numpy, cv2
from PIL import Image
import pygame, pygame.locals

#Pygameの初期化
pygame.init()

########## 変数群 ##########

#スクリーン
Screen = pygame.display.set_mode((1920, 1080))
#スクリーンサイズ
ScreenWidth = Screen.get_width()
ScreenHeight = Screen.get_height()
#背景
BackPic = None
BackPicList = []
BackFlame = 1
#泡
BubbleList = []
BublePic = None
#ベゼル
BEZEL = 50
#初期の魚の数
FISHNUM = 99
#クラスFishが入る
FishList = []
#フレームレート制限用
clock = pygame.time.Clock()
FLAMELATE = 20

Kani = None


########## 関数群 ##########

#初期セットアップを行う関数
def Setup():
    #初期の魚を読み込む処理
    for i in range(FISHNUM):
        FileName = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resource", str(i) + ".png")
        ImageObj = cv2.imread(FileName)
        if ImageObj is not None:
            FishList.append(Fish(ImageObj, False))

    #背景gifに関する処理
    global BackPic, BackPicList
    FileName = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resource", "background.gif")
    BackPic = Image.open(FileName)
    #画像を分割してPygameで読み込む形式に
    for frame in range(0, BackPic.n_frames):
        BackPic.seek(frame)
        frame_surface = pygame.image.fromstring(
            BackPic.tobytes(), BackPic.size, BackPic.mode
        )
        BackPicList.append(frame_surface)
    
    #カニに関する処理
    FileName = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resource", "kani.png")
    KaniPic = cv2.imread(FileName)
    global Kani
    Kani = Fish(KaniPic, True)

    pygame.display.update()
    return

def BackDisplay():
    global BackFlame, blitCounter  # blitCounterもグローバル変数として指定
    
    Screen.blit(BackPicList[BackFlame], (0, 0))
    
    blitCounter += 1  # blitが呼び出されるたびにカウントを増加

    if blitCounter == 24:  # 24回呼び出された場合
        BackFlame += 1
        blitCounter = 0  # カウントをリセット
    
    if 21 < BackFlame:
        BackFlame = 1

def Buble():
    for item in BubbleList:
        item.move()
        item.draw()
    
    if random.randrange(0,4) == 0:
        BubbleList.append(Bubble())

#全てのFishを表示する
def FishDisplay():
    for item in FishList:
        item.Process()
        item.Display()

#終了判定
def LoopOut():
    #ループ抜け処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

########## クラス ##########

# 泡のクラス
class Bubble:
    def __init__(self):
        self.Siz = random.randint(10, 100)  # 泡の半径をランダムに設定
        self.Pic = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "resource", "Buble.png"))
        # x または y が指定されていない場合はランダムな座標を設定
        self.x = random.randint(0, ScreenWidth)
        self.y = ScreenHeight-50
        self.speed = random.randint(3, 10)  # ランダムな速度を設定
        self.angle = random.uniform(-1.1, 1.1)  # 左右にランダムな角度で揺れる
        self.direction_change_prob = 0.4  # 方向転換の確率
        self.frame_count = 0  # フレームカウント
        

    def move(self):
        self.y -= self.speed
        self.x += int(self.angle * 2)  # 揺れる角度で移動
        if random.random() < self.direction_change_prob:
            self.angle *= -1  # 方向転換

        self.frame_count += 1
        # 5フレームごとに半径を減少させる
        if self.frame_count % 5 == 0:
            self.Siz -= 1

    def draw(self):
        if self.Siz < 0 or self.y < -20:
            return
        Pic = pygame.transform.scale(self.Pic, (self.Siz, self.Siz))
        Screen.blit(Pic, (self.x, self.y))

class Fish:

    #コンストラクタ
    def __init__(self, pic, isKani):
        #基本的なメンバー変数
        self.PosX = random.randrange(0, ScreenWidth)
        self.PosY = random.randrange(0, ScreenHeight)
        self.Angle = random.randrange(0, 360)

        #ヒレの動きに関するメンバ変数
        self.FIN_X = 40
        self.Fin_Count = 0
        self.Fin_TargetX = 0
        self.Fin_TargetTY = 0
        self.Fin_TargetBY = 0

        #画像に関するメンバー変数
        self.Pic = pic

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

        self.isKani = isKani

        if self.isKani:
            self.PosY = 300
            self.Angle = 0


    #画面に表示する
    def Display(self):

        def WrapAroundScreen():
            #画面端移動
            if ScreenWidth + BEZEL < self.PosX:
                self.PosX = -BEZEL
            elif self.PosX < 0 - BEZEL:
                self.PosX = ScreenWidth + BEZEL
            
            if ScreenHeight + BEZEL < self.PosY:
                self.PosY = -BEZEL
            elif self.PosY < 0 - BEZEL:
                self.PosY = ScreenHeight + BEZEL

        def ProjectiveTF(pic):
            #射影変換
            #画像を分割
            FinPic = pic[:, :40]
            BodyPic = pic[:, 40:]

            #画像の変数
            FinWidth = FinPic.shape[1]
            FinHeight = FinPic.shape[0]

            #尾ひれの終点X,Yを設定
            if self.Fin_Count < 40:
                #奥→手前
                self.Fin_TargetTY -= 1
                self.Fin_TargetBY += 1
                if self.Fin_Count < 20:
                    self.Fin_TargetX += 1
                else:
                    self.Fin_TargetX -= 1
            else:
                #手前→奥
                self.Fin_TargetTY += 1
                self.Fin_TargetBY -= 1
                if self.Fin_Count < 60:
                    self.Fin_TargetX += 1
                else:
                    self.Fin_TargetX -= 1
            self.Fin_Count += 1
            self.Fin_Count = self.Fin_Count % 80
            

            #マトリックスの作成
            BP1 = [0, 0]
            BP2 = [FinWidth, 0]
            BP3 = [0, FinHeight]
            BP4 = [FinWidth, FinHeight]
            AP1 = [self.Fin_TargetX, self.Fin_TargetTY]
            AP2 = BP2
            AP3 = [self.Fin_TargetX, self.Fin_TargetBY]
            AP4 = BP4
            BeforePoint = numpy.float32((BP1, BP2, BP3, BP4))
            AfterPoint = numpy.float32((AP1, AP2, AP3, AP4))
            Matrix = cv2.getPerspectiveTransform(BeforePoint, AfterPoint)

            #画像の変形
            TransWidth = FinWidth - self.Fin_TargetX
            TransHeigth = self.Fin_TargetBY - self.Fin_TargetTY
            if TransHeigth < FinHeight:
                TransHeigth = FinHeight
            ArrayPic = cv2.warpPerspective(FinPic, Matrix, (TransHeigth, TransWidth))

            def pad_image_center(img, target_height):
                # 上下に追加するパディングの高さを計算
                pad_top = (target_height - img.shape[0]) // 2
                pad_bottom = target_height - img.shape[0] - pad_top
                
                # 画像に上下のパディングを追加
                padded_img = cv2.copyMakeBorder(img, pad_top, pad_bottom, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
                return padded_img

            # 最大の高さを取得
            max_height = max(ArrayPic.shape[0], BodyPic.shape[0])

            # 画像の高さを最大の高さに合わせる
            ArrayPic = pad_image_center(ArrayPic, max_height)
            BodyPic = pad_image_center(BodyPic, max_height)

            #画像をくっつける
            ArrayPic = cv2.hconcat([ArrayPic, BodyPic])
            print("Top = " + str(TransWidth) + "Buttom" + str(TransHeigth))
            return ArrayPic
        
        def make_black_transparent_for_pygame(cv2_img):
            ##00000部分を透過処理し、Pygameで読み込みが可能な形式に変更する by ChatGPT
            # 画像にアルファチャンネルがない場合は追加
            if cv2_img.shape[2] < 4:
                cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2BGRA)

            # 黒色 (#000000) のピクセルを透過処理
            cv2_img[(cv2_img[:, :, 0] == 0) & (cv2_img[:, :, 1] == 0) & (cv2_img[:, :, 2] == 0)] = [0, 0, 0, 0]

            # OpenCVはBGRでイメージを扱うが、pygameはRGBを使用するので変換が必要
            cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGRA2RGBA)
            
            # Numpy arrayからpygameのサーフェスに変換
            height, width = cv2_img.shape[:2]
            pygame_img = pygame.image.fromstring(cv2_img.tostring(), (width, height), 'RGBA')

            return pygame_img
        
        def AdjustAngle():
            #Angleの調整
            self.Angle = self.Angle % 360
            return
        
        def Invert(pic):
            #画像反転
            RePic = pic
            if 90 < self.Angle and self.Angle < 270 and self.isKani == False:
                RePic = pygame.transform.flip(pic, False, True)
            return RePic
        
        def RotateImage(pic):
            #画像の回転
            RotatePic = pygame.transform.rotate(pic, self.Angle * -1)
            #画像の中心点の取得
            PicRect = pic.get_rect()
            CenterX = PicRect.width // 2
            CenterY = PicRect.height // 2
            #画像を中心で回転させて表示する
            RotatedRect = RotatePic.get_rect(center=(self.PosX + CenterX, self.PosY + CenterY))
            return RotatePic, RotatedRect.topleft
        
        ArrayPictuire = self.Pic
        #画面端移動
        WrapAroundScreen()
        #Angleを調整
        AdjustAngle()
        #射影変換
        #ArrayPictuire = ProjectiveTF(ArrayPictuire)
        #CV2の画像をPygameで読み込む形式に変更する
        Picture = make_black_transparent_for_pygame(ArrayPictuire)
        #画像を反転させる
        Picture = Invert(Picture)
        #画像を回転させる
        Picture, Rect = RotateImage(Picture)

        #画像を表示させる
        Screen.blit(Picture, Rect)
        return


    def TanEase(self, targetValue, remainingValue):
        SinIncVal = 90 / (FLAMELATE * 2)
        
        if targetValue * 0.9 < remainingValue:
            #RampUp
            if self.SF_SinEaseCount <= 64:  #64なのは、tan(64)≒2であるため。その為scaleを/2している。
                self.SF_SinEaseCount += SinIncVal
                scale = round(math.tan(math.radians(self.SF_SinEaseCount)) / 2, 2)
            else:
                scale = 1
            return scale, False
        
        elif  remainingValue < targetValue * 0.1:
            #RampDown
            if 0 <= self.SF_SinEaseCount:
                scale = round(math.tan(math.radians(self.SF_SinEaseCount)) / 2, 2)
                self.SF_SinEaseCount -= SinIncVal
                return scale, False
            else:
                #MoveEnd
                scale = 0
                return scale, True
        
        else:
            #FullSpeed
            scale = 1
            return scale, False

    #前進
    def SlowMoveForward(self, distance, speed = -1):

        #一回きりの処理
        if self.SF_IsFirstTime:
            self.SF_SinEaseCount = 0
            self.SF_RemainingValue = distance
            self.SF_IsFirstTime = False

        #Speedの調整
        if speed == -1:
            speed = self.SPEED

        #速度に掛ける"Scale"の設定と終了判定
        Scale, IsEnd = self.TanEase(distance, self.SF_RemainingValue)

        if IsEnd:
            self.SF_IsFirstTime = True
            return True

        #移動先の座標を決定する
        #直進
        XIncreace = math.cos(math.radians(self.Angle)) * speed * Scale
        YIncreace = math.sin(math.radians(self.Angle)) * speed * Scale
        self.PosX += XIncreace
        self.PosY += YIncreace

        #SF_RemainingValueの更新
        self.SF_RemainingValue -= round(math.sqrt(XIncreace ** 2 + YIncreace ** 2), 2)
        
        #画像に対して垂直の角度を取得
        VarticalAngle = self.Angle + 90 % 360

        #Sin波
        self.PosX += (math.sin(math.radians(self.SF_FrequencyCount)) * math.cos(math.radians(VarticalAngle))) * self.AMPLITUDE * Scale
        self.PosY += (math.sin(math.radians(self.SF_FrequencyCount)) * math.sin(math.radians(VarticalAngle))) * self.AMPLITUDE * Scale

        #カウントアップ
        self.SF_FrequencyCount += self.FREQUENCY

        return False


    def QuickMoveForward(self, distance):
        if self.QF_IsFirstTime:
            self.QF_RemainingValue = distance
            self.QF_IsFirstTime = False

        #End
        if self.QF_RemainingValue < 1:
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
        
        #速度に掛ける"Scale"の設定と終了判定
        Scale, IsEnd = self.TanEase(angle, self.SA_RemainingValue)

        if IsEnd:
            self.SA_IsFirstTime = True
            return True
        
        IncreaceValue = 0
        if angle == 0:
            IncreaceValue = 0
        else:
            IncreaceValue = angle / abs(angle) * 2 * Scale
        self.Angle += IncreaceValue
        self.SA_RemainingValue -= IncreaceValue

        #直進
        XIncreace = math.cos(math.radians(self.Angle)) * self.SPEED * Scale
        YIncreace = math.sin(math.radians(self.Angle)) * self.SPEED * Scale
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
                #print("2-1")
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

def test():
    #Screen.blit(BackPic, (0, 0))
    FishList[0].Process()
    FishList[0].Display()

def kani():
    Kani.SlowMoveForward(999999999999)
    Kani.Display()


#初期セットアップ
Setup()
while True:
    #画面のリセット
    Screen.fill((0,0,0))

    #表示する
    BackDisplay()
    FishDisplay()
    kani()
    Buble()
    
    #test()

    #画面の更新とフレームレート制限
    pygame.display.update()
    clock.tick(FLAMELATE)

    #ループ抜け処理
    LoopOut()