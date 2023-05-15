import os
import random
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic, Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
# 더 추가할 필요가 있다면 추가하시면 됩니다. 예: (from PyQt5.QtGui import QIcon)

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('maingame.ui')
form_class = uic.loadUiType(form)[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint) # 프레임 지우기
        self.showFullScreen() #풀스크린 화면 만들기
        # self.exitAction.triggered.connect(qApp.closeAllWindows) # 게임 종료 이벤트

        # TODO 처음 게임 시작했을 때 시작 화면 보여주기
        # {시작버튼 객체}.clicked.connect(lambda: {스택위젯 이름}.setCurrentIndex({일반필드 스택위젯 페이지}))

        # TODO 랜덤확률로 수호대 위치 4군데 중 1군데로 설정시키기 (왼, 오, 위, 아래)
        # x, y 값은 맵 x, y 값으로 수정하기
        # random_spot = random.randrange(1, 4)
        # if random_spot == 1:
        #     self.{캐릭터 들어있는 라벨명}.move(10, 190)
        #     self.{포탈 라벨명}.move(random.randint(340, 620), random.randint(10, 460))
        # if random_spot == 2:
        #     self.{캐릭터 들어있는 라벨명}.move(340, 10)
        #     self.{포탈 라벨명}.move(random.randint(10, 620), random.randint(190, 460))
        # if random_spot == 3:
        #     self.{캐릭터 들어있는 라벨명}.move(340, 460)
        #     self.{포탈 라벨명}.move(random.randint(10, 620), random.randint(10, 190))
        # if random_spot == 4:
        #     self.{캐릭터 들어있는 라벨명}.move(620, 190)
        #     self.{포탈 라벨명}.move(random.randint(10, 340), random.randint(10, 460))

        # 일반필드에서 LCD에 포션 나타내주는 값
        # setText() 는 레이블 내 텍스트 설정 / setNum() 레이블 내 정수를 설정


        # TODO 캐릭터 움직일 때 마다 x, y 좌표 반영하기
        self.character_left_img = QPixmap('character_left.png')
        self.character_right_img = QPixmap('character_right.png')
        self.back_ground_label.setPixmap(QtGui.QPixmap("용암.png"))
        self.widget.move(826,-1)
        self.back_ground_label.move(0,-1)
        self.Status1_1_Class.setText("close")

    #캐릭터 방향키로 움직이기===============================================================================================
    # 다른키를 눌러도 입력값을 받는 문제가 있음 => 어떻게 수정해야 하지?
    def keyPressEvent(self, event):
        rand_event = random.randrange(4)
        if event.key() == Qt.Key_A and self.label.x() > 0:
            self.label.setPixmap(self.character_left_img)
            self.label.move(self.label.x() - 20, self.label.y())
        elif event.key() == Qt.Key_D and self.label.x() < 1580:
            self.label.setPixmap(self.character_right_img)
            self.label.move(self.label.x() + 20, self.label.y())
        elif event.key() == Qt.Key_W and self.label.y() > 0:
            self.label.move(self.label.x(), self.label.y() - 20)
        elif event.key() == Qt.Key_S and self.label.y() < 760:
            self.label.move(self.label.x(), self.label.y() + 20)

        #캐릭터의 x, y 좌표 받아오기
        lab_x_ = self.label.pos().x()
        lab_y_ = self.label.pos().y()

        #랜덤 값에 따라 이동 / 적 만남 / 수호대 만남 / 아이템 획득
        if rand_event == 1 and self.label.x() > 0 and self.label.x() < 1580 and self.label.y() > 0 and self.label.y() < 760: #캐릭터 창 밖으로 넘어가지 못하게 하기
            self.Log_textEdit.append("1칸 이동하였습니다.")
        elif rand_event == 2 and self.label.x() > 0 and self.label.x() < 1580 and self.label.y() > 0 and self.label.y() < 760: #캐릭터 창 밖으로 넘어가지 못하게 하기
            enemy_rand = random.randrange(4)
            if enemy_rand >= 3:
                self.Log_textEdit.append("적을 만났습니다.") #전투 함수로 이동
            elif enemy_rand == 4:
                self.Log_textEdit.append("타 수호대를 만났습니다.") # 전투 함수로 이동
        elif rand_event == 3 and self.label.x() > 0 and self.label.x() < 1580 and self.label.y() > 0 and self.label.y() < 760:
            self.Log_textEdit.append("아이템을 획득하였습니다.")
            # 아이템 획득하면 아이템 라벨 변경해주기
            # 아이템 얻는 함수
            # setText() 는 레이블 내 텍스트 설정 / setNum() 레이블 내 정수를 설정

        ## TODO elif 포탈과 만날시
        ## 포탈 나타나는 랜덤값 설정하기
        ## 포탈 x, y 값 +20 or -20 값 에 들어가면 창 이동하게하기
        ### 일반필드라면 -> 던전 층수 나오는 창 띄우기 -> 클리어한 던전만 활성화 되게 하기
        ### 던전이라면 -> 일반필드 나갈 수 있게 하기

        #왼쪽 상단에 좌표 확인시켜주기
        self.TopUI_Coordinate_Label.setText(f"x좌표: {lab_x_} y좌표: {lab_y_}")

    #def 아이템 얻는 함수(self):
        # 3. 아이템 얻기
        ## 10%의 확률로 텐트 겟
        ## 레벨에 따른 포션 겟
        ## 포션 얻으면 lcd 창에 표시해주기
        #### 직업 변경권은 어떻게 얻더라?

    #def let_user_know_portal_loacation(self)  #유저가 포탈 위치 알게 되는 함수
        # self.{던전포탈위치상태} = True
        # def lab_hide(self):
        #  """던전에서 포탈 위치 보여주는 함수"""
        #     if self.{던전포탈위치상태} ==  True:
        #         self.{던전포탈위치상태} = False
        #         self.{배경위검은라벨}.hide()
        #     else:
        #         self.{던전포탈위치상태} = True
        #         self.{배경위검은라벨}.show()

    #def 전투함수(self):
        #전투로 창이동시키기
        # self.변경할_스택위젯이름.setCurrentIndex(변경할_페이지)

        ## 일반몬스터 만났을 때
        ### 몬스터, 캐릭터 정보 들어가게 하기 (+ hp, mp 정보도) <- 혜빈이 오늘 한거 붙여넣기하기
        ### 전투 시작하면 캐릭터 장비를 각각의 스택위젯 창에 업데이트 시키기 -> 이건 해야함

        #### 일반공격 선택시 -> hp 가 0초과인 몬스터 버튼 활성화 -> 공격력 25%로 먹이기 -> 상태창에 얼마나 데미지 입혔는지 띄우기 ->  몬스터가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> 아군 중 전투가능이 없으면(hp 가 모두 없다면 전투 실패)
        #### 스킬 선택시 -> 위젯 띄우기 -> 캐릭터의 정보가 불러와져서 캐릭터의 스킬만 활성화 -> 클릭하면 몬스터에 공격 데미지 상태창에 표시 -> 몬스터가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> hp가 모두 없다면 전투 실패
        #### 아이템 선택시 -> 장비 및 소비 창 활성화
        ##### 소비창 버튼 클릭하면 선택한 캐릭터 mp hp 영향 -> 상태창에 띄우기 -> hpmp 라벨 변경 -> 몬스터가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> 다음 캐릭터가 없으면 상대턴으로 넘어감
        ##### 장비창 버튼 클릭하면 각 캐릭터 콤보박스 이동 -> 강화석 있다면 +버튼 활성화 -> (+)버튼 누르면 장비 업그레이드, 상태창에 정보 띄우기
        #### 회피 선택시 - 30%의 확률로 회피 성공. -> 몬스터가 다 죽지 않았다면 -> 다음 캐릭터로 턴이동. 마지막 캐릭터일시 1번 캐릭터로 -> hpmp가 모두 없다면 전투 실패

        ##수호대 만났을 때
        ## 수호대 정보 들어가게 하기
        ## 수호대, 캐릭터 정보 들어가게 하기
        #### 공격 선택시 -> hp 가 0초과인 수호대 버튼 활성화 -> 공격력 랜덤으로 먹이기 -> 상태창에 얼마나 데미지 입혔는지 띄우기 ->  수호대가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> hp 가 모두 없다면 전투 실패
        #### 스킬 선택시 -> 스택 위젯 띄우기 -> 캐릭터의 정보가 불러와져서 캐릭터의 스킬만 활성화 -> 클릭하면 수호대 공격 데미지 상태창에 표시 -> 수호대가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> hpmp가 모두 없다면 전투 실패
        #### 아이템 선택시 -> 장비 및 소비 창 활성화
        ##### 소비창 버튼 클릭하면 캐릭터 mp hp 영향 -> 수호대가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> hpmp가 모두 없다면 전투 실패
        ##### 장비창 버튼 클릭하면 각 캐릭터 콤보박스 이동 -> 강화석 있다면 +버튼 활성화 ->[ 장비가 노발 장비라면 하급 강화석 필요, 레어 장비라면 상급 강화석 필요. ]->(+)버튼 누르면 장비 업그레이드, 상태창에 정보 띄우기
        #### 회피 선택시 - 몇 프로의 확률로 회피 성공. -> 몬스터가 다 죽지 않았다면 -> 다음 캐릭터로 턴이동. 마지막 캐릭터일시 1번 캐릭터로 -> hpmp가 모두 없다면 전투 실패

    #def 승리함수(self, 이긴위치):
        #승리했을 때 어떤 상황에 따라 어떤 보상을 줄 지 선택하기




# ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    # 게임 종료 이벤트
    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'EXIT', '정말 게임을 종료하시겠습니까?',
    #                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()
# └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass( )
    myWindow.show( )
    app.exec_( )