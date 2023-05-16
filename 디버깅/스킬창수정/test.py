import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *

# from maingame import Ui_Maingame as maingame

import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('maingame.ui')
form_class = uic.loadUiType(form)[0]


class Status:
    def __init__(self, class_name, character_name, hp, mp, level):
        self.class_name = class_name
        self.character_name = character_name
        self.hp = hp
        self.mp = mp
        self.level = level

    def get_classname(self):
        return self.class_name

    def get_charactername(self):
        return self.character_name

    def get_hp(self):
        return self.hp * self.level

    def get_level(self):
        return self.level

    def get_mp(self):
        return self.mp


class MainGame(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 위젯 스킬 창 투명화
        self.Widget_Skill.hide()

        self.user_turn = 0
        self.mon_turn = 0

        # 캐릭터 별 프레임
        self.frame_class_list = [self.Frame_Class1_Status, self.Frame_Class2_Status,
                                 self.Frame_Class3_Status, self.Frame_Class4_Status, self.Frame_Class5_Status]
        # 스킬 버튼 가져오기
        self.skill_btn_set = self.Widget_Skill.findChildren(QPushButton)
        # self.skill_list = []
        # for i in self.skill_btn_set:
        #     self.skill_list.append(i.objectName())
            # self.skill_btn_list = sorted(self.skill_list)      # 순서 정렬
        # print(self.skill_btn_list)
        # print(self.skill_list)
        # 스킬 레이아웃 가져오기
        self.Widget_Skill_set = self.Widget_Skill.findChildren(QGraphicsWidget)

        # 캐릭터별 스킬 버튼 가져오기
        # # 루미너스
        # self.Frame_Class2_set = self.Frame_Class2.findChildren(QPushButton)
        # # 알렉스
        # self.Frame_Class3_set = self.Frame_Class3.findChildren(QPushButton)
        # # 샐래맨더
        # self.Frame_Class4_set = self.Frame_Class4.findChildren(QPushButton)
        # # 메르데스
        # self.Frame_Class5_set = self.Frame_Class5.findChildren(QPushButton)
        # # 랜슬롯
        # self.Frame_Class6_set = self.Frame_Class6.findChildren(QPushButton)

        # 캐릭터 이름 리스트
        self.character_name = ['미하일', '루미너스', '알렉스', '샐러맨더', '메르데스', '랜슬롯']

        class_1 = Status('전사', '미하일', 300, 0, 1)
        class_2 = Status('백법사', '루미너스', 200, 150, 1)
        class_3 = Status('흑법사', '알렉스', 200, 150, 1)
        class_4 = Status('적법사', '샐러맨더', 150, 150, 1)
        class_5 = Status('궁수', '메르데스', 150, 150, 1)
        class_6 = Status('검사', '랜슬롯', 150, 150, 1)
        list_class = [class_1, class_2, class_3, class_4, class_5, class_6]
        random.shuffle(list_class)

        for i in range(5):
            getattr(self, f'Status{i+1}_1_Class').setText(list_class[i].class_name)     # 클래스명 지정
            getattr(self, f'Status{i+1}_1_Class').setAlignment(Qt.AlignCenter)          # 텍스트 가운데 정렬
            getattr(self, f'Status{i+1}_1_Class').setStyleSheet('QLabel{background-color:#55aaff;}')     # 클래스 배경 색상 지정
            getattr(self, f'Status{i+1}_1_Name').setText(list_class[i].character_name)      # 캐릭터명 지정
            getattr(self, f'Status{i+1}_1_Name').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i+1}_2_HpValue').setText(str(list_class[i].hp)+"/"+str(list_class[i].get_hp()))  # hp(기본 값/변하는 값)
            getattr(self, f'Status{i+1}_2_HpValue').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i+1}_3_MpValue').setText(str(list_class[i].mp)+"/"+str(list_class[i].get_mp()))  # mp(기본 값/변하는 값)
            getattr(self, f'Status{i+1}_3_MpValue').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i+1}_2_Hp').setStyleSheet('QLabel{background-color:#55aaff;}')       # hp, mp 배경 색상 지정
            getattr(self, f'Status{i+1}_3_Mp').setStyleSheet('QLabel{background-color:#55aaff;}')

        # 캐릭터 창 초기 [0] 빼고 비활성화 상태
        for FCS in self.frame_class_list[1:]:
            FCS.setEnabled(False)

        # 몬스터 초기 전체 비활성화 상태
        for mon in range(10):
            getattr(self, f'Monster_{mon + 1}_QButton').setEnabled(False)

        # 스킬 초기 전체 비활성화 상태
        # for skill in self.skill_btn_set:
        #     skill.setEnabled(False)
        # 이건 레이아웃을 비활성화 함
        # for skill in self.Widget_Skill_set:
        #     skill.setEnabled(False)

        # 스킬창 모두 비활성화
        for i in range(5):
            getattr(self, f'Frame_Class{i + 1}').setEnabled(False)

        # 버튼 선택에 대한 시그널 연결
        for btn in range(5):
            getattr(self, f'Status{btn + 1}_Action1_Attack').clicked.connect(self.Attack_btn)
            # getattr(self, f'Status{btn + 1}_Action2_Skill').clicked.connect(lambda state, index_ = btn + 1: self.skill_btn(index_))
            getattr(self, f'Status{btn + 1}_Action2_Skill').setCheckable(True)
            getattr(self, f'Status{btn + 1}_Action3_Item').clicked.connect(self.Item_btn)
            getattr(self, f'Status{btn + 1}_Action4_Run').clicked.connect(self.Run_btn)

        # 몬스터 버튼 선택에 대한 시그널 연결
        for mon in range(10):
            if getattr(self, f'Monster_{mon + 1}_QButton').clicked.connect(self.Turn):
                break
            else:
                pass


        #### 여기가 문제 입니다 #### =============================================================

        name_text = self.Status1_1_Name.text()
        skills = {
            '미하일': 1,
            '루미너스': 2,
            '알렉스': 3,
            '샐러맨더': 4,
            '메르데스': 5,
            '랜슬롯': 6
        }

        for name, index in skills.items():
            if name == name_text:
                print(name)
                self.Status1_Action2_Skill.clicked.connect(lambda x, index_=index: self.skill_btn(index_))
                break

        # if '미하일' in self.Status1_1_Name.text():
        #     print(self.Status1_1_Name.text())
        #     print('미하일')
        #     # index_ += 1
        #     # self.Status1_Action2_Skill.clicked.connect(self.skill_btn)
        #     self.Status1_Action2_Skill.clicked.connect(lambda x, index_ = 1 : self.skill_btn(index_))
        #
        # elif '루미너스' in self.Status1_1_Name.text():
        #     print('루미너스')
        #     # index_ += 2
        #     # self.Status1_Action2_Skill.clicked.connect(self.skill_btn)
        #     self.Status1_Action2_Skill.clicked.connect(lambda x, index_ = 2 : self.skill_btn(index_))
        #
        # elif '알렉스' in self.Status1_1_Name.text():
        #     print('알렉스')
        #     # self.index_ += 3
        #     # self.Status1_Action2_Skill.clicked.connect(self.skill_btn)
        #     self.Status1_Action2_Skill.clicked.connect(lambda x, index_= 3: self.skill_btn(index_))
        #
        # elif '샐러맨더' in self.Status1_1_Name.text():
        #     print('샐러맨더')
        #     # self.index_ += 4
        #     # self.Status1_Action2_Skill.clicked.connect(self.skill_btn)
        #     self.Status1_Action2_Skill.clicked.connect(lambda x, index_= 4: self.skill_btn(index_))
        #
        # elif '메르데스' in self.Status1_1_Name.text():
        #     print('메르데스')
        #     # self.index_ += 5
        #     # self.Status1_Action2_Skill.clicked.connect(self.skill_btn)
        #     self.Status1_Action2_Skill.clicked.connect(lambda x, index_= 5: self.skill_btn(index_))
        # elif '랜슬롯' in self.Status1_1_Name.text():
        #     print('랜슬롯')
        #     # self.index_ += 6
        #     # self.Status1_Action2_Skill.clicked.connect(self.skill_btn)
        #     self.Status1_Action2_Skill.clicked.connect(lambda x, index_= 6: self.skill_btn(index_))

       ########=========================================================================


# ====== 함수 ============================================================================================================

    # 공격 버튼 시 몬스터 버튼 활성화
    def Attack_btn(self):
        for mon in range(10):
            getattr(self, f'Monster_{mon + 1}_QButton').setEnabled(True)

    #### 여기가 문제입니다####=================================================================

    def skill_btn(self, index_):
        """스킬번호 받아서 스킬창 활성화/비활성화 하는 함수"""
        self.Widget_Skill.show()
        frames = [
            self.Frame_Class1,
            self.Frame_Class2,
            self.Frame_Class3,
            self.Frame_Class4,
            self.Frame_Class5
        ]
        for idx, frame in enumerate(frames):
            if idx == index_ - 1:
                frame.setEnabled(True) # 해당 스킬 프레임만 활성화
            else:
                frame.setEnabled(False) # 그 이외는 비활성화
        self.Attack_btn()
        print('skill')

    # def skill_btn(self, index_):
    #     # print(self.index_)
    #     if index_ == 1:
    #         self.Widget_Skill.show()
    #         self.Frame_Class1.setEnabled(True)
    #         self.Attack_btn()
    #     elif index_ == 2:
    #         self.Widget_Skill.show()
    #         self.Frame_Class2.setEnabled(True)
    #         self.Attack_btn()
    #     elif index_ == 3:
    #         self.Widget_Skill.show()
    #         self.Frame_Class3.setEnabled(True)
    #         self.Attack_btn()
    #     elif index_ == 4:
    #         self.Widget_Skill.show()
    #         self.Frame_Class4.setEnabled(True)
    #         self.Attack_btn()
    #     elif index_ == 5:
    #         self.Widget_Skill.show()
    #         self.Frame_Class5.setEnabled(True)
    #         self.Attack_btn()
    #     print('skill')
     ########============================================================================

    def Item_btn(self):
        print('Item')

    def Run_btn(self):
        print('Run')

    def Turn(self):
        """몬스터 공격 버튼 눌렀을 때 함수"""
        self.user_turn += 1  # 유저 턴에 대한 초기 설정

        if self.user_turn >= len(self.frame_class_list): #6번 돌리면 초기화 해줌 if self.user_turn >= 6:
            self.user_turn = 0

        for idx, FCS in enumerate(self.frame_class_list):
            if self.user_turn == idx:
                FCS.setEnabled(True)
                # print('유저 활성화')
            else:
                FCS.setEnabled(False)
                # print('유저 비활성화')

        for mon in range(10): #몬스터 버튼 비활성화
            getattr(self, f'Monster_{mon + 1}_QButton').setEnabled(False)

        self.Widget_Skill.hide()

        for i in range(5):
            getattr(self, f'Frame_Class{i + 1}').setEnabled(False) #스킬창 모두 비활성화

        for j in range(5):
            print('스킬 버튼 비활성화 시키고 싶다...')
            if self.user_turn < 4:
                print(self.user_turn)
                getattr(self, f'Status{j + 1}_Action2_Skill').setCheckable(True) # 클래스 각각의 스킬버튼 활성화
                print('이게 되나..?')
                pass
            else:
                getattr(self, f'Status{j + 1}_Action2_Skill').setCheckable(False)
                print('스킬 버튼 비활성화')



class MainGame(QMainWindow, form_class):
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = MainGame()
        ex.show()
        app.exec_()