import os
import random
import sys
import time

from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import uic, Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt, QByteArray, QSize, QTimer

from maingame import Ui_Maingame as game


class Status:
    """
    직업 상속 클래스
    """

    def __init__(self, class_name, character_name, hp, mp, level, class_img):
        self.class_name = class_name
        self.character_name = character_name
        self.hp = hp
        self.mp = mp
        self.level = level
        self.class_img = class_img

    def get_classname(self):
        """클래스 이름"""
        return self.class_name

    def get_charactername(self):
        """캐릭터 이름"""
        return self.character_name

    def get_maxhp(self):
        """max_hp 반환"""
        return self.hp * self.level  # 반환 hp = 기존 hp * level

    def get_nowhp(self):
        """현재 hp"""
        return self.get_maxhp()  # max_hp값 리턴

    def get_level(self):
        """클래스 레벨"""
        return self.level

    def get_maxmp(self):
        """최대 mp"""
        return self.mp * self.level  # mp* 레벨 리턴

    def get_image(self):
        """캐릭터 이미지"""
        return self.class_img


class MonsterOption:
    """
    몬스터 상속 클래스: 몬스터 필드/ 이름/ 이미지/ 레벨/ hp/ 공격력
    """

    def __init__(self, field, name, img, level, hp, atk):
        """몬스터 필드/ 이름/ 이미지/ 레벨/ hp/ 공격력"""
        self.field = field
        self.name = name
        self.image = img
        self.level = level
        self.hp = hp
        self.atk = atk

    def get_field(self):
        """소속 필드"""
        return self.field

    def get_name(self):
        """몬스터 이름"""
        return self.name

    def get_image(self):
        """몬스터 이미지"""
        return self.image

    def get_level(self):
        """몬스터 레벨"""
        return self.level

    def get_hp(self):
        """몬스터 체력"""
        return self.hp

    def get_atk(self):
        """몬스터 공격력"""
        return self.atk


class SkillOption:
    """
    스킬 상속 클래스: 이름, 이미지, 데미지 값, 소비mp(스킬마나), 스킬 종류, ??
    """

    def __init__(self, name, img, value, mp, target, turn):
        self.name = name
        self.img = img
        self.value = value
        self.mp = mp
        self.target = target
        self.turn = turn

    def get_name(self):
        """스킬 이름"""
        return self.name

    def get_img(self):
        """스킬 이미지"""
        return self.img

    def get_value(self):
        """스킬 데미지 값"""
        return self.value

    def get_target(self):
        """스킬 종류 구별(버프, 단일, 전체)"""
        return self.target

    def get_mp(self):
        """스킬 마나"""
        return self.mp

    def get_turn(self):
        """몰루<--??오잉"""
        return self.turn

class ItemMain:
    """ 아이템 상속 클래스(부모)"""
    def __init__(self, item_name):
        super().__init__()

        self.name = item_name

    def get_name(self):
        return self.name


class Equipment(ItemMain):
    """ 장비 아이템 상속 클래스"""
    def __init__(self, name, item_location):
        super().__init__(name)

        self.location = item_location

    def get_item_location(self):
        return self.location

class Weapon(Equipment):
    """ 무기 아이템 상속 클래스"""
    def __init__(self, name, location, weapon_damage):
        super().__init__(name, location)

        self.damage = weapon_damage

    def get_weapon_damage(self):
        return self.damage

class Armor(Equipment):
    """ 장비 아이템 상속 클래스"""
    def __init__(self, name, location, armor_defence):
        super().__init__(name, location)

        self.armor = armor_defence

    def get_armor_defence(self):
        return self.armor


class Consumable(ItemMain):
    """ 소비 아이템 상속 클래스"""
    def __init__(self, name, recovery, stack):
        super().__init__(name)
        self.recovery = recovery
        self.stack = stack

    def get_recovery_value(self):
        return self.recovery

    def get_stack(self):
        return self.stack


# 소비 아이템 변수 지정
item_consumable_hp_S = Consumable("HP포션 (소)", 50, 10)
item_consumable_hp_M = Consumable("HP포션 (중)", 100, 0)
item_consumable_hp_L = Consumable("HP포션 (대)", 150, 0)
item_consumable_mp_S = Consumable("MP포션 (소)", 50, 10)
item_consumable_mp_M = Consumable("MP포션 (중)", 100, 0)
item_consumable_mp_L = Consumable("MP포션 (대)", 150, 0)
item_consumable_all_S = Consumable("All포션 (소)", 0.25, 0)
item_consumable_all_M = Consumable("All포션 (중)", 0.5, 0)
item_consumable_all_L = Consumable("All포션 (대)", 1, 0)
item_consumable_resurrection = Consumable('부활포션', 1, 0)
item_consumable_tent = Consumable('텐트', 1, 0)
item_consumable_change = Consumable('직업변경권', 0, 5)
item_consumable_enhancement_low = Consumable('강화석 하급', 0, 0)
item_consumable_enhancement_high = Consumable('강화석 상급', 0, 0)

# 무기 순서 : 검(0) 방패(3) 숏스태프(6) 롱스태프(9) 룬스태프(12) 보우(15)
weapon_list = [Weapon('조잡한 검', '무기', 10), Weapon('튼튼한 검', '무기', 20), Weapon('보키 검', '무기', 40),
               Weapon('가죽 방패', '방패', 10), Weapon('사슬 방패', '방패', 20), Weapon('철 방패', '방패', 40),
               Weapon('조잡한 숏스태프', '무기', 10), Weapon('튼튼한 숏스태프', '무기', 20),  Weapon('보키 숏스태프', '무기', 40),
               Weapon('조잡한 롱스태프', '무기', 10), Weapon('튼튼한 롱스태프', '무기', 20), Weapon('보키 롱스태프', '무기', 40),
               Weapon('조잡한 룬스태프', '무기', 10), Weapon('튼튼한 룬스태프', '무기', 20), Weapon('보키 룬스태프', '무기', 40),
               Weapon('조잡한 보우', '무기', 10), Weapon('튼튼한 보우', '무기', 20), Weapon('보키 보우', '무기', 40)]

head_list = [Armor('허름한 천두건', '머리', 5), Armor('튼튼한 천두건', '머리', 10), Armor('보키 천두건', '머리', 20),
             Armor('조잡한 가죽투구', '머리', 10), Armor('튼튼한 가죽투구', '머리', 15), Armor('보키 가죽투구', '머리', 30),
             Armor('조잡한 철투구', '머리', 15), Armor('튼튼한 철투구', '머리', 20), Armor('보키 철투구', '머리', 40)]

armor_list = [Armor('허름한 천갑옷', '상의', 10), Armor('튼튼한 천갑옷', '상의', 20), Armor('보키 천갑옷', '상의', 40),
              Armor('허름한 가죽갑옷', '상의', 15), Armor('튼튼한 가죽갑옷', '상의', 30), Armor('보키 가죽갑옷', '상의', 60),
              Armor('조잡한 중갑옷', '상의', 25), Armor('튼튼한 중갑옷', '상의', 50), Armor('보키 중갑옷', '상의', 100),
              Armor('조잡한 경갑옷', '상의', 20), Armor('튼튼한 경갑옷', '상의', 40), Armor('보키 경갑옷', '상의', 80)]

pants_list = [Armor('허름한 천바지', '하의', 10), Armor('튼튼한 천바지', '하의', 12), Armor('보키 천바지', '하의', 14),
              Armor('허름한 가죽바지', '하의', 12), Armor('튼튼한 가죽바지', '하의', 14), Armor('보키 가죽바지', '하의', 16),
              Armor('허름한 중갑바지', '하의', 16), Armor('튼튼한 중갑바지', '하의', 18), Armor('보키 중갑바지', '하의', 20),
              Armor('허름한 경갑바지', '하의', 14), Armor('튼튼한 경갑바지', '하의', 16), Armor('보키 경갑바지', '하의', 18)]

glove_list = [Armor('허름한 천장갑', '장갑', 5), Armor('튼튼한 천장갑', '장갑', 7), Armor('보키 천장갑', '장갑', 9),
              Armor('허름한 가죽장갑', '장갑', 7), Armor('튼튼한 가죽장갑', '장갑', 9), Armor('보키 가죽장갑', '장갑', 11),
              Armor('허름한 사슬장갑', '장갑', 9), Armor('견고한 사슬장갑', '장갑', 11), Armor('보키 사슬장갑', '장갑', 13)]

cloak_list = [Armor('허름한 천망토', '망토', 5), Armor('튼튼한 천망토', '망토', 10), Armor('보키 천망토', '망토', 15),
              Armor('허름한 가죽망토', '망토', 10), Armor('튼튼한 가죽망토', '망토', 15), Armor('보키 가죽망토', '망토', 20)]

class_warrior = [head_list[6], armor_list[6], pants_list[6], glove_list[6],
                 weapon_list[0], weapon_list[3], cloak_list[3]]

class_whitewizard = [head_list[0], armor_list[0], pants_list[0], glove_list[0],
                     weapon_list[6], weapon_list[3], cloak_list[0]]

class_blackwizard = [head_list[0], armor_list[0], pants_list[0], glove_list[0],
                     weapon_list[9], weapon_list[3], cloak_list[0]]

class_redwizard = [head_list[3], armor_list[3], pants_list[3], glove_list[3],
                   weapon_list[12], weapon_list[3], cloak_list[3]]

class_archer = [head_list[3], armor_list[3], pants_list[3], glove_list[3],
                weapon_list[15], None, cloak_list[3]]

class_swordman = [head_list[3], armor_list[9], pants_list[9], glove_list[3],
                  weapon_list[0], None, cloak_list[3]]

list_consumable = [item_consumable_hp_S, item_consumable_hp_M, item_consumable_hp_L,
                   item_consumable_mp_S, item_consumable_mp_M, item_consumable_mp_L,
                   item_consumable_all_S, item_consumable_all_M, item_consumable_all_L,
                   item_consumable_resurrection, item_consumable_tent, item_consumable_change,
                   item_consumable_enhancement_low, item_consumable_enhancement_high]
class WindowClass(QMainWindow, game):
    """
    메인 게임 진행
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 일단 임시로 옮겨놓음
        # for i in range(1, 6):
        #     getattr(self, f"Status{i}_Action1_Attack").clicked.connect(lambda : self.attack_function(i))

        self.Status1_Action1_Attack.clicked.connect(lambda: self.attack_function(1))
        self.Status2_Action1_Attack.clicked.connect(lambda: self.attack_function(2))
        self.Status3_Action1_Attack.clicked.connect(lambda: self.attack_function(3))
        self.Status4_Action1_Attack.clicked.connect(lambda: self.attack_function(4))
        self.Status5_Action1_Attack.clicked.connect(lambda: self.attack_function(5))

        self.Status1_Action3_Item.clicked.connect(lambda: self.Iteam_function(1))
        self.Status2_Action3_Item.clicked.connect(lambda: self.Iteam_function(2))
        self.Status3_Action3_Item.clicked.connect(lambda: self.Iteam_function(3))
        self.Status4_Action3_Item.clicked.connect(lambda: self.Iteam_function(4))
        self.Status5_Action3_Item.clicked.connect(lambda: self.Iteam_function(5))

        self.Status1_Action4_Run.clicked.connect(lambda: self.Run_function(1))
        self.Status2_Action4_Run.clicked.connect(lambda: self.Run_function(2))
        self.Status3_Action4_Run.clicked.connect(lambda: self.Run_function(3))
        self.Status4_Action4_Run.clicked.connect(lambda: self.Run_function(4))
        self.Status5_Action4_Run.clicked.connect(lambda: self.Run_function(5))


        # 몬스터 버튼 클릭하면 몬스터 공격 함수로 넘어감
        # for j in range(1, 11):
        #     getattr(self, f"Monster_{j}_QButton").clicked.connect(lambda: self.monster_got_damage(j))
        self.Monster_1_QButton.clicked.connect(lambda x: self.monster_got_damage(1))
        self.Monster_2_QButton.clicked.connect(lambda x: self.monster_got_damage(2))
        self.Monster_3_QButton.clicked.connect(lambda x: self.monster_got_damage(3))
        self.Monster_4_QButton.clicked.connect(lambda x: self.monster_got_damage(4))
        self.Monster_5_QButton.clicked.connect(lambda x: self.monster_got_damage(5))
        self.Monster_6_QButton.clicked.connect(lambda x: self.monster_got_damage(6))
        self.Monster_7_QButton.clicked.connect(lambda x: self.monster_got_damage(7))
        self.Monster_8_QButton.clicked.connect(lambda x: self.monster_got_damage(8))
        self.Monster_9_QButton.clicked.connect(lambda x: self.monster_got_damage(9))
        self.Monster_10_QButton.clicked.connect(lambda x: self.monster_got_damage(10))

        # 공격 타입 구분 초기 설정값
        self.attackType = 0

        # 유저 턴 구분 초기 설정값
        self.user_turn = 0
        self.class_alive = []
        self.class_turn = [1, 2, 3, 4, 5]

        # ui 하단 버튼 비활성화
        for i in range(1, 6):
            getattr(self, f'Status{i}_Action1_Attack').setEnabled(False)
            getattr(self, f'Status{i}_Action2_Skill').setEnabled(False)
            getattr(self, f'Status{i}_Action3_Item').setEnabled(False)
            getattr(self, f'Status{i}_Action4_Run').setEnabled(False)

        # 혜빈 코드 취합 본 시작===========================================================================================

        # 해당 인스턴스에 캐릭터 정보 저장
        self.guardLevel = 1
        self.TopUI_Level_Label.setText("%s의 수호대 Level : %d" % ("땅", self.guardLevel))

        self.guardoption()  # 캐릭터 생성해줌
        self.StautsHpall = []
        self.StautsMpall = []
        self.Statusclass = []

        # 리스트를 셔플로 돌려줌
        # 위 self.guardoption()에서 생성한 클래스 캐릭터들의 값총 6개-(전체정보/최대hp/최대mp)저장
        random.shuffle(self.list_class)

        # 유저 체력을 리스트에 담아준다.
        self.class_hp_dict = {}
        self.class_mp_dict = {}
        for i in range(1, 7):  # 서플로 돌려준 클래스유저들의 체력을 빈 딕셔너리에 1부터 6까지 담아줌 <- 수정함
            self.class_hp_dict[i] = self.list_class[i - 1][1]
        for i in range(1, 7):  # 서플로 돌려준 클래스유저들의 마나를 빈 딕셔너리에 1부터 6까지 담아줌 <- 수정함
            self.class_mp_dict[i] = self.list_class[i - 1][2]

        print('유저 체력 확인용', self.class_hp_dict)

        # 위에서 섞은 list_class을 프레임에 1부터 5까지 가져와 담아줌
        for i in range(1, 6):
            # 빈 리스트에 추가
            self.Statusclass.append(self.list_class[i - 1][0])  # 빈 리스트 Statusclass에 하나씩 전체정보를 append해줌
            self.StautsHpall.append(self.list_class[i - 1][1])  # 빈 리스트 StautsHpall에 하나씩 최대hp를 append해줌
            self.StautsMpall.append(self.list_class[i - 1][1])  # 빈 리스트 StautsMpall에 하나씩 최대mp를 append해줌

            # 하단 ui에 캐릭터 추가
            getattr(self, f'Status{i}_1_Class').setText(self.list_class[i - 1][0].class_name)  # 클래스명 지정
            getattr(self, f'Status{i}_1_Name').setText(self.list_class[i - 1][0].character_name)  # 캐릭터명 지정
            getattr(self, f'Status{i}_2_HpValue').setText(
                str(self.list_class[i - 1][1]) + "/" + str(self.list_class[i - 1][0].get_maxhp()))  # hp(기본 값/변하는 값)
            getattr(self, f'Status{i}_3_MpValue').setText(
                str(self.list_class[i - 1][2]) + "/" + str(self.list_class[i - 1][0].get_maxmp()))  # mp(기본 값/변하는 값)
            getattr(self, f'Class_{i}_QLabel').setPixmap(QtGui.QPixmap(self.list_class[i - 1][3]))

            # 정렬 및 스타일시트 배경 디자인
            getattr(self, f'Status{i}_2_HpValue').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i}_1_Name').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i}_3_MpValue').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i}_1_Class').setAlignment(Qt.AlignCenter)  # 텍스트 가운데 정렬
            getattr(self, f'Status{i}_1_Class').setStyleSheet('QLabel{background-color:#55aaff;}')  # 클래스 배경 색상 지정
            getattr(self, f'Status{i}_2_Hp').setStyleSheet('QLabel{background-color:#55aaff;}')  # hp, mp 배경 색상 지정
            getattr(self, f'Status{i}_3_Mp').setStyleSheet('QLabel{background-color:#55aaff;}')

        # 캐릭터 별 프레임
        self.frame_class_list = [self.Frame_Class1_Status, self.Frame_Class2_Status,
                                 self.Frame_Class3_Status, self.Frame_Class4_Status, self.Frame_Class5_Status]
        self.itemusebox = [] # 아이템 버튼 담기는 박스
        for btn in range(1, 15):
            self.itemusebox.append(getattr(self, f'Portion_{btn}_Btn'))
        for idx, cont in enumerate(self.itemusebox): #아이템 버튼 연결
            cont.clicked.connect(lambda x, y=idx + 1: self.Iteam_name(y))
        # 혜빈 코드 취합 본 끝 ============================================================================================
        """길준이 형님 취합 - 코드 시작 findnum:0921"""
        # 아이템 코드 취합 시작 ===========================================================================================
        # 아이템 프리셋 호출
        self.item_class_1 = class_warrior
        self.item_class_2 = class_whitewizard
        self.item_class_3 = class_blackwizard
        self.item_class_4 = class_redwizard
        self.item_class_5 = class_archer
        self.item_class_6 = class_swordman
        # 아이템 프리셋 호출 후 리스트 작성
        self.hp_s = item_consumable_hp_S
        self.hp_m = item_consumable_hp_M
        self.hp_l = item_consumable_hp_L
        self.mp_s = item_consumable_mp_S
        self.mp_m = item_consumable_mp_M
        self.mp_l = item_consumable_mp_L
        self.all_s = item_consumable_all_S
        self.all_m = item_consumable_all_M
        self.all_l = item_consumable_all_L
        self.resurrection = item_consumable_resurrection
        self.tent = item_consumable_tent
        self.change = item_consumable_change
        self.enhancement_low = item_consumable_enhancement_low
        self.enhancement_high = item_consumable_enhancement_high

        self.item_list = [self.hp_s, self.hp_m, self.hp_l, self.mp_s, self.mp_m, self.mp_l,
                          self.all_s, self.all_m, self.all_l, self.resurrection, self.tent, self.change,
                          self.enhancement_low, self.enhancement_high]

        self.class_item_list()
        print(self.class_item[0][4].name)

        self.class_name_reset()

        for i in range(len(self.list_class)):
            if self.list_class[0][0] == getattr(self, f'class_{i + 1}'):
                first_page = i + 1
        self.first_page = first_page
        self.combobox_add()
        self.status_page_reset()

        # 장비 업그레이드용 카운터
        self.item_class_upgrade_counter_1 = [0, 0, 0, 0, 0, 0, 0]
        self.item_class_upgrade_counter_2 = [0, 0, 0, 0, 0, 0, 0]
        self.item_class_upgrade_counter_3 = [0, 0, 0, 0, 0, 0, 0]
        self.item_class_upgrade_counter_4 = [0, 0, 0, 0, 0, 0, 0]
        self.item_class_upgrade_counter_5 = [0, 0, 0, 0, 0, 0, 0]
        self.item_class_upgrade_counter_6 = [0, 0, 0, 0, 0, 0, 0]
        self.upgrade_index = 0  # 장비 강화 캐릭터 선택을 위한 페이지 인덱스 값

        self.StackWidget_Equip.setCurrentWidget(getattr(self, f'Class_{first_page}_Equip_Page'))
        self.get_index()
        self.item_upgrade_button_reset()
        self.Btn_Equip.setEnabled(False)
        self.Btn_Portion.setEnabled(True)
        self.Btn_Status.setEnabled(True)

        self.Btn_Portion.clicked.connect(lambda: self.StackWidget_Item.setCurrentWidget(self.Page_Use))
        self.Btn_Portion.clicked.connect(self.use_page)
        self.Btn_Equip.clicked.connect(lambda: self.StackWidget_Item.setCurrentWidget(self.Page_Equip))
        self.Btn_Equip.clicked.connect(self.equip_page)
        self.Btn_Equip.clicked.connect(self.get_index)
        self.Btn_Equip.clicked.connect(self.item_upgrade_button_reset)
        self.Btn_Status.clicked.connect(lambda: self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing))
        self.Btn_Status.clicked.connect(self.status_page)
        self.consumable_reset()

        # 콤보박스 선택에 따라 장비창 변환
        self.ComboBox_Class.activated[str].connect(self.class_equip_page)
        self.ComboBox_Class.activated[str].connect(self.get_index)  # 장비강화 캐릭터 선택을 위한 페이지 인덱스 값 추출

        # 장비강화
        self.item_upgrade_button_reset()
        for i in range(6):
            getattr(self, f'Equip{i + 1}_1Helmet_Btn').clicked.connect(self.helmet_upgrade)
        for i in range(6):
            getattr(self, f'Equip{i + 1}_2_Armor_Btn').clicked.connect(self.armor_upgrade)
        for i in range(6):
            getattr(self, f'Equip{i + 1}_3_Pants_Btn').clicked.connect(self.pants_upgrade)
        for i in range(6):
            getattr(self, f'Equip{i + 1}_5_Hand_Btn').clicked.connect(self.glove_upgrade)
        for i in range(6):
            getattr(self, f'Equip{i + 1}_6_Weapon_Btn').clicked.connect(self.weapon_upgrade)
        for i in range(6):
            getattr(self, f'Equip{i + 1}_7_Shield_Btn').clicked.connect(self.shield_upgrade)
        for i in range(6):
            getattr(self, f'Equip{i + 1}_8_Cloak_Btn').clicked.connect(self.cloak_upgrade)

        # 포션 사용
        self.Portion_1_Btn.clicked.connect(self.hp_using_1)
        self.Portion_2_Btn.clicked.connect(self.hp_using_2)
        self.Portion_3_Btn.clicked.connect(self.hp_using_3)
        self.Portion_4_Btn.clicked.connect(self.mp_using_1)
        self.Portion_5_Btn.clicked.connect(self.mp_using_2)
        self.Portion_6_Btn.clicked.connect(self.mp_using_3)
        self.Portion_7_Btn.clicked.connect(self.all_using_1)
        self.Portion_8_Btn.clicked.connect(self.all_using_2)
        self.Portion_9_Btn.clicked.connect(self.all_using_3)
        self.Portion_10_Btn.clicked.connect(self.revive_using)
        self.Portion_11_Btn.clicked.connect(self.tent_use)
        self.Portion_12_Btn.clicked.connect(self.class_change_using)

        """길준이 형님 취합 - 코드 종료"""
        # ++ keypressevent 함수에 추가로 추합
        # ==================================================================================================================

        # 몬스터 상속 - 몬스터 필드/ 이름/ 이미지/ 레벨/ hp/ 공격력(임시로100)
        # 변경사항""""""""변경사항""""""""변경사항""""""""변경사항""""""""변경사항""""""""변경사항""""""""변경사항""""""""
        """배경 모음"""
        self.nomalfield_fire_background = ["./배경/fire_1.png", "./배경/fire_2.png", "./배경/fire_3.png"]
        self.nomalfield_ice_background = ["./배경/ice_1.png", "./배경/ice_2.png", "./배경/ice_3.png"]
        self.nomalfield_forest_background = ["./배경/forest_1.png", "./배경/forest_2.png", "./배경/forest_3.png"]
        self.nomalfield_water_background = ["./배경/water_1.png", "./배경/water_2.png", "./배경/water_3.png"]
        self.nomalfield_backgroundBox = [self.nomalfield_fire_background, self.nomalfield_ice_background,
                                         self.nomalfield_forest_background, self.nomalfield_water_background]
        """불의 지역 몬스터들"""
        self.nomalfield_fire_monster1 = MonsterOption("불의 지역", "흔하게 생긴 불돼지", "./MonsterImage/fire_1.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.nomalfield_fire_monster2 = MonsterOption("불의 지역", "불의 골렘", "./MonsterImage/fire_2.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.nomalfield_fire_monster3 = MonsterOption("불의 지역", "불의 정령", "./MonsterImage/fire_3.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.nomalfield_fire_monster4 = MonsterOption("불의 지역", "불에 익지않는 크랩", "./MonsterImage/fire_4.png", 1,
                                                      random.randrange(200, 1000), 50)

        """눈의 지역 몬스터들"""
        self.nomalfield_ice_monster1 = MonsterOption("눈의 지역", "눈의 정령", "./MonsterImage/ice_1.png", 1,
                                                     random.randrange(200, 1000), 50)
        self.nomalfield_ice_monster2 = MonsterOption("눈의 지역", "눈속에서 타오르는 불", "./MonsterImage/ice_2.png", 1,
                                                     random.randrange(200, 1000), 50)
        self.nomalfield_ice_monster3 = MonsterOption("눈의 지역", "몰루판다", "./MonsterImage/ice_3.png", 1,
                                                     random.randrange(200, 1000), 50)
        self.nomalfield_ice_monster4 = MonsterOption("눈의 지역", "눈보라를 날리는 양", "./MonsterImage/ice_4.png", 1,
                                                     random.randrange(200, 1000), 50)

        """대지의 지역 몬스터들"""
        self.nomalfield_forest_monster1 = MonsterOption("대지의 지역", "흔한 번데기", "./MonsterImage/forest_1.png", 1,
                                                        random.randrange(200, 1000), 50)
        self.nomalfield_forest_monster2 = MonsterOption("대지의 지역", "늙은 장수풍뎅이", "./MonsterImage/forest_2.png", 1,
                                                        random.randrange(200, 1000), 50)
        self.nomalfield_forest_monster3 = MonsterOption("대지의 지역", "억울한 슬라임", "./MonsterImage/forest_3.png", 1,
                                                        random.randrange(200, 1000), 50)
        self.nomalfield_forest_monster4 = MonsterOption("대지의 지역", "어딘가 위험한 식물", "./MonsterImage/forest_4.png", 1,
                                                        random.randrange(200, 1000), 50)

        """물의 지역 몬스터들"""
        self.nomalfield_water_monster1 = MonsterOption("물의 지역", "탁한 기운의 도룡뇽", "./MonsterImage/water_1.png", 1,
                                                       random.randrange(200, 1000), 50)
        self.nomalfield_water_monster2 = MonsterOption("물의 지역", "단단한 붕어", "./MonsterImage/water_2.png", 1,
                                                       random.randrange(200, 1000), 50)
        self.nomalfield_water_monster3 = MonsterOption("물의 지역", "위험해보이는 붕어", "./MonsterImage/water_3.png", 1,
                                                       random.randrange(200, 1000), 50)
        self.nomalfield_water_monster4 = MonsterOption("물의 지역", "그냥 상어", "./MonsterImage/water_4.png", 1,
                                                       random.randrange(200, 1000), 50)

        """던전 필드 몬스터들"""
        self.dugeonfield_1st_monster1 = MonsterOption("던전 1층", "킬러비", "./MonsterImage/dugeonmonster_1.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster2 = MonsterOption("던전 1층", "던전 박쥐", "./MonsterImage/dugeonmonster_2.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster3 = MonsterOption("던전 2층", "평범한 슬라임", "./MonsterImage/dugeonmonster_3.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster4 = MonsterOption("던전 2층", "차가운 슬라임", "./MonsterImage/dugeonmonster_4.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster5 = MonsterOption("던전 3층", "외눈박이 촉수 문어", "./MonsterImage/dugeonmonster_5.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster6 = MonsterOption("던전 3층", "푸른 킬러 플라워", "./MonsterImage/dugeonmonster_6.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster7 = MonsterOption("던전 4층", "그린 드래곤", "./MonsterImage/dugeonmonster_7.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster8 = MonsterOption("던전 4층", "히드라", "./MonsterImage/dugeonmonster_8.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster9 = MonsterOption("던전 5층", "레드 드래곤", "./MonsterImage/dugeonmonster_9.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster10 = MonsterOption("던전 5층", "붉은 킬러 플라워", "./MonsterImage/dugeonmonster_10.png", 1,
                                                       random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster11 = MonsterOption("던전 6층", "독침 전갈", "./MonsterImage/dugeonmonster_11.png", 1,
                                                       random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster12 = MonsterOption("던전 6층", "베젤부부의 하수인", "./MonsterImage/dugeonmonster_12.png", 1,
                                                       random.randrange(200, 1000), 50)
        """던전 보스 몬스터"""
        self.dugeonfield_Boss1 = MonsterOption("던전 1층", "이동려크", "./MonsterImage/dugeonBoss_1.png", 1,
                                               random.randrange(200, 1000), 50)
        self.dugeonfield_Boss2 = MonsterOption("던전 2층", "조동혀니", "./MonsterImage/dugeonBoss_2.png", 1,
                                               random.randrange(200, 1000), 50)
        self.dugeonfield_Boss3 = MonsterOption("던전 3층", "류홍보기", "./MonsterImage/dugeonBoss_3.png", 1,
                                               random.randrange(200, 1000), 50)
        self.dugeonfield_Boss4 = MonsterOption("던전 4층", "코로나 공주", "./MonsterImage/dugeonBoss_4.png", 1,
                                               random.randrange(200, 1000), 50)
        self.dugeonfield_Boss5 = MonsterOption("던전 5층", "이땅보키", "./MonsterImage/dugeonBoss_5.png", 1,
                                               random.randrange(200, 1000), 50)
        self.dugeonfield_Boss6 = MonsterOption("던전 6층", "환생한 보키", "./MonsterImage/dugeonBoss_6.png", 1,
                                               random.randrange(200, 1000), 50)
        self.dugeonfield_Boss7 = MonsterOption("던전 7층", "로드 오브 보키", "./MonsterImage/dugeonBoss_7.png", 1,
                                               random.randrange(200, 1000), 50)

        """상속받은 이미지와 이미지값을 담은 리스트들을 한곳에 담아주기"""
        self.firemonsterbox = [self.nomalfield_fire_monster1, self.nomalfield_fire_monster2,
                               self.nomalfield_fire_monster3,
                               self.nomalfield_fire_monster4]

        self.icemonsterbox = [self.nomalfield_ice_monster1, self.nomalfield_ice_monster2, self.nomalfield_ice_monster3,
                              self.nomalfield_ice_monster4]

        self.forestmonsterbox = [self.nomalfield_forest_monster1, self.nomalfield_forest_monster2,
                                 self.nomalfield_forest_monster3,
                                 self.nomalfield_forest_monster4]

        self.watermonsterbox = [self.nomalfield_water_monster1, self.nomalfield_water_monster2,
                                self.nomalfield_water_monster3,
                                self.nomalfield_water_monster4]
        self.nomalfieldallBox = [self.firemonsterbox, self.icemonsterbox, self.forestmonsterbox, self.watermonsterbox]

        self.dugeonfieldbox = [self.dugeonfield_1st_monster1, self.dugeonfield_1st_monster2,
                               self.dugeonfield_1st_monster3, self.dugeonfield_1st_monster4,
                               self.dugeonfield_1st_monster5, self.dugeonfield_1st_monster6,
                               self.dugeonfield_1st_monster7, self.dugeonfield_1st_monster8,
                               self.dugeonfield_1st_monster9, self.dugeonfield_1st_monster10,
                               self.dugeonfield_1st_monster11, self.dugeonfield_1st_monster12]
        self.dugeonBosbox = [self.dugeonfield_Boss1, self.dugeonfield_Boss2, self.dugeonfield_Boss3,
                             self.dugeonfield_Boss4, self.dugeonfield_Boss5, self.dugeonfield_Boss6,
                             self.dugeonfield_Boss7]
        # 변경사항""""""""변경사항""""""""변경사항""""""""변경사항""""""""변경사항""""""""변경사항""""""""변경사항""""""""

        # 스킬 상속 이후 리턴 값으로 리스트 줌
        self.skillbox()

        ## 임시 캐릭터 설정

        self.character_left_img = QPixmap('character_left.png')  # 캐릭터 왼쪽 이미지
        self.character_right_img = QPixmap('character_right.png')  # 캐릭터 오른쪽 이미지

        ## 배경 및 위젯 설정
        self.back_ground_label.setPixmap(QtGui.QPixmap("용암.png"))  # 임시 일반 필드 배경 이미지
        self.back_ground_label.move(0, -1)  # 배경 위치 조정
        self.Widget_Skill.move(826, -1)  # 전투중 스킬 선택시 생성되는 스킬 위젯 위치
        self.Widget_Skill.hide()  # 위젯창은 숨겨 둠

        # 헤더 프레임 없애고 전체화면으로 띄우기
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        # self.exitAction.triggered.connect(qApp.closeAllWindows) # 게임 종료 이벤트

        # self.HoldSwitch = 0
        # self.Page_Use_ing.setEnabled(False)  # 캐릭터 세부정보창 비활성화(우측 상단 index-1)
        # # self.Page_Equip.setEnabled(False)
        # self.Btn_Equip.clicked.connect(lambda y: self.use_uiABC(4))  # 우측 상단 장비 버튼 클릭하면 장비창 이동
        # self.Btn_Portion.clicked.connect(lambda y: self.use_uiABC(0))  # 포션버튼 클릭하면 포션 이동
        # self.Btn_Status.clicked.connect(lambda y: self.use_uiABC(2))  # 캐릭터 세부 장비 활성화

        # # 여기서부터 봐야 함
        for num in range(1, 6):  # 액션버튼 1~4 시그널 슬롯 연결
            #     getattr(self, f'Status{num}_Action1_Attack').clicked.connect(
            #         lambda x, y=num: self.nomalact(y))  # 일반공격함수로 연결
            getattr(self, f'Status{num}_Action2_Skill').clicked.connect(
                lambda x, y=num: self.skillopen(y))  # 스킬옵션 함수로 연결
        #     getattr(self, f'Status{num}_Action3_Item').clicked.connect(lambda y: self.use_uiABC(1))

        # 클래스 스킬 버튼들 리스트화 /
        # #미하일 도발스킬 / #루미너스 스킬: 힐, 그레이트힐, 힐올, 공격력업, 방어력업, 맵핵 / #알렉스 스킬: 파이어볼, 파이어월, 블리자드, 썬더브레이커 / # 메르데스 집중타, 듀얼샷, 마스터샷 / #샐리멘더 힐, 그레이트힐, 힐올, 파이어볼 파이어월, 블리자드 썬더브레이커
        self.pushbox = [self.Class2_Skill1_Btn, self.Class2_Skill2_Btn, self.Class2_Skill3_Btn,
                        self.Class2_Skill4_Btn, self.Class2_Skill5_Btn, self.Class2_Skill6_Btn,
                        self.Class3_Skill1_Btn, self.Class3_Skill2_Btn, self.Class3_Skill3_Btn, self.Class3_Skill4_Btn,
                        self.Class4_Skill1_Btn, self.Class4_Skill2_Btn, self.Class4_Skill3_Btn,
                        self.Class4_Skill4_Btn, self.Class4_Skill5_Btn, self.Class4_Skill6_Btn, self.Class4_Skill7_Btn,
                        self.Class5_Skill1_Btn, self.Class5_Skill2_Btn, self.Class5_Skill3_Btn,
                        self.Class6_Skill1_Btn, self.Class1_Skill1_Btn]  # 강타

        # 수호대 스폰 지역 랜덤 설정 및 미궁 랜덤 생성 (조건 = 무조건 수호대 스폰 지역 반대 편에 포탈 나오게함)========================
        random_spot = random.randrange(1, 5)
        if random_spot == 1:  # 숲의 지역 스폰 장소
            self.Character_QLabel.setPixmap(self.character_left_img)
            self.Character_QLabel.move(100, 520)
            self.TopUI_Map_Label.setText("숲의 지역")
        elif random_spot == 2:  # 불의 지역 스폰 장소
            self.Character_QLabel.setPixmap(self.character_left_img)
            self.Character_QLabel.move(360, 40)
            self.TopUI_Map_Label.setText("불의 지역")
        elif random_spot == 3:  # 눈의 지역 스폰 장소
            self.Character_QLabel.setPixmap(self.character_left_img)
            self.Character_QLabel.move(1280, 20)
            self.TopUI_Map_Label.setText("눈의 지역")
        elif random_spot == 4:  # 물의 지역 스폰 장소
            self.Character_QLabel.setPixmap(self.character_left_img)
            self.Character_QLabel.move(1320, 540)
            self.TopUI_Map_Label.setText("물의 지역")

        # 왼쪽 상단에 초기 죄표 값 출력
        self.TopUI_Coordinate_Label.setText(
            f"x좌표: {self.Character_QLabel.pos().x()} y좌표: {self.Character_QLabel.pos().y()}")

    def guardoption(self):
        """캐릭터 생성 및 hp/mp 저장"""
        self.class_1 = Status('전사', '미하일', 300, 0, self.guardLevel, "./캐릭터 및 수호대/class_1.png")
        self.class_2 = Status('백법사', '루미너스', 200, 150, self.guardLevel, "./캐릭터 및 수호대/class_2.png")
        self.class_3 = Status('흑법사', '알렉스', 200, 150, self.guardLevel, "./캐릭터 및 수호대/class_3.png")
        self.class_4 = Status('적법사', '샐러맨더', 150, 150, self.guardLevel, "./캐릭터 및 수호대/class_4.png")
        self.class_5 = Status('궁수', '메르데스', 150, 150, self.guardLevel, "./캐릭터 및 수호대/class_5.png")
        self.class_6 = Status('검사', '랜슬롯', 150, 150, self.guardLevel, "./캐릭터 및 수호대/class_6.png")

        self.class1_nowhp = self.class_1.get_maxhp()
        self.class2_nowhp = self.class_2.get_maxhp()
        self.class3_nowhp = self.class_3.get_maxhp()
        self.class4_nowhp = self.class_4.get_maxhp()
        self.class5_nowhp = self.class_5.get_maxhp()
        self.class6_nowhp = self.class_6.get_maxhp()

        self.class1_nowmp = self.class_1.get_maxmp()
        self.class2_nowmp = self.class_2.get_maxmp()
        self.class3_nowmp = self.class_3.get_maxmp()
        self.class4_nowmp = self.class_4.get_maxmp()
        self.class5_nowmp = self.class_5.get_maxmp()
        self.class6_nowmp = self.class_6.get_maxmp()
        self.list_class = [[self.class_1, self.class1_nowhp, self.class1_nowmp, self.class_1.class_img],
                           [self.class_2, self.class2_nowhp, self.class2_nowmp, self.class_2.class_img],
                           [self.class_3, self.class3_nowhp, self.class3_nowmp, self.class_3.class_img],
                           [self.class_4, self.class4_nowhp, self.class4_nowmp, self.class_4.class_img],
                           [self.class_5, self.class5_nowhp, self.class5_nowmp, self.class_5.class_img],
                           [self.class_6, self.class6_nowhp, self.class6_nowmp, self.class_6.class_img]]
        return self.list_class

    def skillbox(self):
        """
        스킬 상속 이후 리턴 값으로 리스트 줌
        :return:
        """

        # SkillOption 클래스: 이름, 이미지, 데미지 값, 소비mp(스킬마나), 스킬 종류(0-버프, 1-단일, 2-전체), ??
        self.skill_1 = SkillOption("힐", None, random.randrange(30, 71), 10, 0, 1)
        self.skill_2 = SkillOption("그레이트 힐", None, random.randrange(60, 101), 20, 0, 1)
        self.skill_3 = SkillOption("힐 올", None, random.randrange(40, 81), 10, 0, 1)
        self.skill_4 = SkillOption("공격력 Up", None, random.randrange(30, 70), 10, 0, 1)
        self.skill_5 = SkillOption("방어력 Up", None, random.randrange(30, 70), 10, 0, 1)
        self.skill_6 = SkillOption("맵 핵", None, 0, 0, 1, 1)

        self.skill_7 = SkillOption("파이어 볼", "검사버프스킬 모션-1.gif", 300, 10, 1, 1)
        self.skill_8 = SkillOption("파이어 월", None, random.randrange(400, 600), 10, 2, 1)
        self.skill_9 = SkillOption("썬더브레이커", None, random.randrange(400, 500), 10, 2, 1)
        self.skill_10 = SkillOption("블리자드", None, random.randrange(900, 1200), 10, 2, 1)

        self.skill_11 = SkillOption("집중타", None, random.randrange(200, 500), 10, 1, 1)
        self.skill_12 = SkillOption("듀얼 샷", None, random.randrange(400, 600), 10, 1, 1)
        self.skill_13 = SkillOption("마스터 샷", None, random.randrange(500, 700), 10, 1, 1)

        self.skill_14 = SkillOption("강타", None, random.randrange(20, 500), 10, 1, 1)
        self.skill_15 = SkillOption("도발", None, 0, 10, 3, 1)
        self.skillall = [self.skill_1, self.skill_2, self.skill_3, self.skill_4, self.skill_5, self.skill_6,
                         self.skill_7, self.skill_8, self.skill_9, self.skill_10, self.skill_11,
                         self.skill_12, self.skill_13, self.skill_14, self.skill_15]

        # 스킬들을 담아서 return 해줌
        return self.skillall

    # 신규함수 ========================================================================================================================

        # 몬스터가 랜덤 등장하는 부분
    def Add_Monster_info(self):
        # MonsterRand
        """MonsterImage 랜덤 등장 구현"""
        self.j = 1
        monster_random_num = random.randrange(2, 11)  # MonsterImage 랜덤 등장 숫자
        self.monster_hp_dict = {}  # 빈 딕셔너리에 MonsterImage 체력 담기
        list_fieldname = ["불", "눈", "숲", "물"]
        list_namecolor = ["Color : white", "Color : red", "Color : white", "Color : white"]
        for idx, fieldname in enumerate(list_fieldname):
            if fieldname == self.user_location(self.lab_x_, self.lab_y_):
                self.monrand = random.randrange(0, 3)
                self.back_ground_label.setPixmap(QtGui.QPixmap(self.nomalfield_backgroundBox[idx][self.monrand]))
                self.namecolor = list_namecolor[idx]
        for num in range(1, monster_random_num):
            for idx, field in enumerate(list_fieldname):
                if field == self.user_location(self.lab_x_, self.lab_y_):
                    self.monrand = random.randrange(0, 4)
                    self.monster = self.nomalfieldallBox[idx][self.monrand]
            getattr(self, f'Monster_{num}_Name').setText(self.monster.name)  # MonsterImage 이름
            getattr(self, f'Monster_{num}_Name').setStyleSheet(self.namecolor)
            getattr(self, f'Monster_{num}_QLabel').setPixmap(QPixmap(self.monster.image))  # MonsterImage 이미지
            getattr(self, f'Monster_{num}_QProgressBar').setMaximum(self.monster.hp)  # MonsterImage 체력
            self.monster_hp_dict[num] = self.monster.hp  # MonsterImage 체력 더하기
            getattr(self, f'Monster_{num}_QProgressBar').setValue(self.monster.hp)  # MonsterImage 체력
            getattr(self, f'Monster_{num}_QButton').setEnabled(False)
            getattr(self, f'Monster_{num}_Name').show()
            getattr(self, f'Monster_{num}_QLabel').show()
            getattr(self, f'Monster_{num}_QButton').show()
            getattr(self, f'Monster_{num}_QProgressBar').show()

            if self.j < 3:
                self.j += 1
            else:
                self.j = 1
        print("몬스터체력", self.monster_hp_dict)

        for num in range(monster_random_num, 10 + 1):
            getattr(self, f'Monster_{num}_Name').hide()
            getattr(self, f'Monster_{num}_QLabel').hide()
            getattr(self, f'Monster_{num}_QButton').hide()
            getattr(self, f'Monster_{num}_QProgressBar').hide()

    # 전투 시작
    # 유저 턴 시작
    def User_Turn(self):
        """유저 턴이었을 때"""
        ############################일반필드나가기 ####################################
        if all(h == 0 for h in self.class_hp_dict.values()):
            print('되나')
            self.Log_textEdit.append('유저 체력이 부족하여 후퇴합니다...')
            self.go_to_normalfield()  # 유저가 전부 죽으면 체력 회복
            # 12341234
            # 체력회복하고 레벨감소

            self.StackWidget_Field.setCurrentIndex(0)  # 일반필드로 이동
            return
        print('유저턴', self.user_turn)
        ## 유저 턴 확인

        if self.user_turn >= 5:  # 만약 유저 턴이 5보다 크다면
            self.user_turn = 1  # 1로 만들어준다.
            self.monster_attack_users()  # 이거 여기다 넣으니까 (동시 다발적으로 캐릭터가 죽으면 턴이 넘어가도 몬스터가 공격을안함) 이 현상이 해결됨..

        else:
            self.user_turn += 1  # 그렇지 않다면 턴 더해주기
        print('현재 턴은', self.user_turn)  # 확인용

        # 유저턴 hp 0 이상이면 활성화 / 아니면 다음 턴으로 넘어감
        selected_character_hp = self.class_hp_dict[self.user_turn]  # 선택된 캐릭터의 hp
        if selected_character_hp > 0:
            self.active_class_frame(self.user_turn)  # 해당 클래스 버튼들 활성화 및 다른 프레임 버튼들 비활성화

        else:
            self.User_Turn()  # 0보다 작으면 다시 User_Turn 돌아감 (재귀함수)

    def go_to_normalfield(self):
        # 사용하지말아봐
        # 만약 모든 유저 hp가 0이면 일반필드로 나가게 함
        if all(h == 0 for h in self.class_hp_dict.values()):
            #
            #     self.class_turn = [1, 2, 3, 4, 5]  # class_turn 초기화 해주고
            #     for i in range(1, 6):  # 서플로 돌려준 클래스유저들의 체력을 빈 딕셔너리에 1부터 5까지 다시 담아주고
            #         self.class_hp_dict[i] = self.list_class[i - 1][1]
            #         self.class_mp_dict[i] = self.list_class[i - 1][2]
            #         getattr(self, f'Status{i}_2_HpValue').setText(
            #             str(self.class_hp_dict[i]) + "/" + str(self.list_class[i - 1][1].get_maxhp()))  # hp(기본 값/변하는 값)
            #         getattr(self, f'Status{i}_3_MpValue').setText(
            #             str(self.class_mp_dict[i]) + "/" + str(self.list_class[i - 1][0].get_maxmp()))  # mp(기본 값/변하는 값)
            #     print('유저 체력 확인용', self.class_hp_dict) #해줘 응애

            self.Log_textEdit.append('유저 체력이 부족하여 후퇴합니다...')
            self.StackWidget_Field.setCurrentIndex(0)  # 일반필드로 이동
            return

        if all(v == 0 for v in self.monster_hp_dict.values()):
            self.guardLevel += 1
            print("현재 레벨 %d"%self.guardLevel)
            self.TopUI_Level_Label.setText("%s의 수호대 Level : %d"%("땅", self.guardLevel))
            print("몬스터 체력이 0입니다.")
            self.Log_textEdit.append('몬스터를 모두 처치했습니다....')
            self.StackWidget_Field.setCurrentIndex(0)  # 일반필드로 이동
            return

    def skillopen(self, num):
        """스킬 함수(스킬 버튼 외 다른 버튼 비활성화, 몬스터 공격 버튼 활성화) # 일단 기존 함수 제외하고 쓰는중"""
        # 스킬 버튼 외에 다른 버튼 비활성화
        self.attackType = 1
        getattr(self, f'Status{num}_Action1_Attack').setEnabled(False)
        getattr(self, f'Status{num}_Action3_Item').setEnabled(False)
        getattr(self, f'Status{num}_Action4_Run').setEnabled(False)
        self.Widget_Skill.show()
        for rockbtn in self.pushbox:
            rockbtn.setEnabled(True)
        for idx, skillbtn in enumerate(self.pushbox):
            skillbtn.clicked.connect(lambda x, y=idx + 1: self.btnname(y))

    def btnname(self, obnum):
        """스킬 선택 관련 버튼 타겟 0이면 아군 적용 타겟 1이면 적군 단일 적용 타겟 2면 적군 전체 적용"""
        for skillbtn in self.pushbox:
            skillbtn.disconnect()

        self.dict_skillname = {1: "힐", 2: "그레이트 힐", 3: "힐 올", 4: "공격력 업", 5: "방어력 업", 6: "맵핵", 7: "파이어 볼",
                               8: "파이어 월",
                               9: "블리자드", 10: "썬더브레이커", 11: "힐", 12: "그레이트 힐", 13: "힐 올", 14: "파이어 볼", 15: "파이어 월",
                               16: "블리자드", 17: "썬더브레이커", 18: "집중타", 19: "듀얼 샷", 20: "마스터 샷", 21: "강타", 22: "도발"}
        self.dict_skill_damage = {"힐": 0, "그레이트 힐": 0, "힐 올": 0, "공격력 업": 0, "방어력 업": 0, "맵핵": 0, "파이어 볼": 100,
                                  "파이어 월": 200, "블리자드": 300, "썬더브레이커": 400, "집중타": 100, "듀얼 샷": 200, "마스터 샷": 300,
                                  " 강타": 500, "도발": 0}
        self.choice_btn = self.dict_skillname[obnum]
        print("내가 클릭한 버튼 값 :%d" % obnum)
        print(self.choice_btn)

        for skill in self.skillall:
            if self.choice_btn == skill.name and skill.target == 0:
                self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
                self.Page_Use_ing.setEnabled(True)
                self.monster_btn_active(False)
                for i in range(6):
                    getattr(self, f'Class_{i+1}_Btn').clicked.connect(lambda x, y=i+1: self.skill_heal(y))
            elif skill.name == self.choice_btn and skill.target >= 1:
                self.monster_btn_active(True)
        self.Log_textEdit.append(self.pushbox[obnum - 1].text() + "을(를) 선택하셨습니다.")
        for rockbtn in self.pushbox:
            rockbtn.setEnabled(False)

    def skillact(self):
        """스킬 선택했을때 그 스킬이름과 같은 데미지가 적용하게 하는 함수
        순서 : 스킬 버튼을 클릭한다 -> self.choice_btn에 스킬이름이 담긴다 -> 이 함수에서 스킬 데미지로 치환한다."""
        self.skillbox()
        if self.choice_btn != 0:
            for skill in self.skillall:
                if ((skill.name == self.choice_btn)
                        and (skill.target == 1)):
                    self.choice_btn = skill.value
                    print(self.choice_btn)
                    return 1
                elif ((skill.name == self.choice_btn)
                      and (skill.target == 2)):
                    self.choice_btn = skill.value
                    return 2
                elif ((skill.name == self.choice_btn)
                      and (skill.target == 3)):
                    return 3
                elif ((skill.name == self.choice_btn)
                      and (skill.target == 0)): # 스킬 타겟이 0번일때 페이지 이동하면서 그 페이지 활성화
                    self.choice_btn = skill.value
                    return 0

    def skill_heal(self, num):
        if self.choice_btn == '힐':
            heal_rate = self.skill_1.value/100
            self.class_hp_dict[num] = self.class_hp_dict[num] + (self.list_class[num-1][0].get_maxhp() * heal_rate)
            print(self.list_class[num-1][0].get_maxhp() * heal_rate)
            print(self.list_class[num-1][0].get_maxhp())
            if self.class_hp_dict[num] > self.list_class[num-1][0].get_maxhp():
                self.class_hp_dict[num] = self.list_class[num-1][0].get_maxhp()
            self.Log_textEdit.append('%s의 체력을 %d%% 회복하였습니다' %
                                     (self.list_class[num-1][0].character_name, int(heal_rate*100)))
        elif self.choice_btn == '그레이트 힐':
            great_heal_rate = self.skill_2.value/100
            self.class_hp_dict[num] = self.class_hp_dict[num] + (self.list_class[num-1][0].get_maxhp() * great_heal_rate)
            if self.class_hp_dict[num] > self.list_class[num-1][0].get_maxhp():
                self.class_hp_dict[num] = self.list_class[num-1][0].get_maxhp()
            self.Log_textEdit.append('%s의 체력을 %d%% 회복하였습니다' %
                                     (self.list_class[num - 1][0].character_name, int(great_heal_rate * 100)))
        elif self.choice_btn == '힐 올':
            all_heal_rate = self.skill_3.value/100
            alive_class = [key for key, value in self.class_hp_dict.items() if value > 0]
            for i in range(len(alive_class)):
                if self.class_hp_dict[i] == 0:
                    pass
                else:
                    self.class_hp_dict[i] = self.class_hp_dict[i] + (self.list_class[i][0].get_maxhp() * all_heal_rate)
                if self.class_hp_dict[i] > self.list_class[i][0].get_maxhp():
                    self.class_hp_dict[i] = self.list_class[i][0].get_maxhp()
                self.Log_textEdit.append('아군 전체의 체력을 %d%% 회복하였습니다' % int(all_heal_rate * 100))
        self.status_page_reset()
        self.low_ui_reset()


    def attack_function(self, num):
        """공격 함수(공격버튼 외 다른 버튼 비활성화, 몬스터 공격버튼 활성화)"""
        self.attackType = 0
        self.Log_textEdit.append(f"클래스 {num}번이 공격버튼을 선택했습니다.")
        self.name = [self.list_class[0][0].character_name, self.list_class[1][0].character_name,
                     self.list_class[2][0].character_name, self.list_class[3][0].character_name,
                     self.list_class[4][0].character_name, self.list_class[5][0].character_name]
        selection_class = self.name.index(getattr(self, f'Status{num}_1_Name').text())+1
        self.choice_btn = int(getattr(self, f'Class{selection_class}_DetailsStatus_AtkValue').text())
        print(self.name)
        print(selection_class)
        print(getattr(self, f'Status{num}_1_Name').text())
        print("클래스의 이름은?? : "+getattr(self, f'Class{selection_class}_DetailsStatus_Name').text())
        print("클래스의 공격력 : %d"%int(getattr(self, f'Class{selection_class}_DetailsStatus_AtkValue').text()))

        # fixfind
        # 공격 버튼 외에 다른 버튼 비활성화
        getattr(self, f'Status{num}_Action2_Skill').setEnabled(False)
        getattr(self, f'Status{num}_Action3_Item').setEnabled(False)
        getattr(self, f'Status{num}_Action4_Run').setEnabled(False)

        # 몬스터 공격 버튼 활성화
        self.monster_btn_active(True)

    def Iteam_function(self, num):
        """아이템 선택시 나머지 버튼 잠김"""
        self.Page_Use.setEnabled(True)
        self.Log_textEdit.append(f"클래스 {num}번이 아이템버튼을 선택했습니다.")
        getattr(self, f'Status{num}_Action1_Attack').setEnabled(False)
        getattr(self, f'Status{num}_Action2_Skill').setEnabled(False)
        getattr(self, f'Status{num}_Action4_Run').setEnabled(False)

    def Iteam_name(self, num):
        """아이템 선택시 발동되는 함수"""
        self.Log_textEdit.append(getattr(self, f'Portion_{num}_Btn').text()) # 해당 아이템 클릭시 상호작용 확인용


    def Run_function(self, num):
        self.Log_textEdit.append(f"클래스 {num}번이 도망버튼을 선택했습니다.")
        if self.user_turn >= 5:
            self.user_turn = 0
            self.monster_attack_users()
            return
        self.User_Turn()

        getattr(self, f'Status{num}_Action1_Attack').setEnabled(False)
        getattr(self, f'Status{num}_Action2_Skill').setEnabled(False)
        getattr(self, f'Status{num}_Action3_Item').setEnabled(False)

    def monster_got_damage(self, num):

        """몬스터 데미지 입는 함수"""
        if self.attackType == 1:
            self.target = self.skillact()

            if self.target == 2:
                for i in range(1, len(self.monster_hp_dict.keys()) + 1):
                    self.monster_hp_dict[i] -= self.choice_btn
            elif self.target == 1:
                self.monster_hp_dict[num] -= self.choice_btn
            elif self.target == 3:
                self.Log_textEdit.append("아무일도 없었다..")
            self.Widget_Skill.close()
        elif self.attackType == 0:
            self.monster_hp_dict[num] -= self.choice_btn  # 임시로 몬스터 체력에는 100씩 데미지 입힘

        print(f'{num}번 몬스터의 맞은 후 체력: {self.monster_hp_dict[num]}')  # 확인용

        self.go_to_normalfield()

        # 체력 0인 얘들은 안보여주기
        for m, n in self.monster_hp_dict.items():
            if n < 0:
                print(f'{m}번 몬스터를 처치했습니다.')  # 콘솔 확인용

                self.Log_textEdit.append(f'{m}번 몬스터를 처치했습니다.')

                self.monster_hp_dict[m] = 0

                # 죽은 몬스터 구성들은 숨겨주기
                getattr(self, f'Monster_{m}_Name').hide()
                getattr(self, f'Monster_{m}_QLabel').hide()
                getattr(self, f'Monster_{m}_QButton').hide()
                getattr(self, f'Monster_{m}_QProgressBar').hide()

        if all(v == 0 for v in self.monster_hp_dict.values()):
            self.guardLevel += 1 # 적을 모두처치하면 레벨업 +1
            print("현재 레벨 %d" % self.guardLevel)
            self.TopUI_Level_Label.setText("%s의 수호대 Level : %d" % ("땅", self.guardLevel))
            print("몬스터 체력이 0입니다.")
            self.Log_textEdit.append('몬스터를 모두 처치했습니다....')
            self.StackWidget_Field.setCurrentIndex(0)  # 일반필드로 이동

        # 프로그래스바에 유저가 때린 몬스터 체력 넣어주기
        getattr(self, f'Monster_{num}_QProgressBar').setValue(self.monster_hp_dict[num])  # 몬스터 체력

        # 몬스터 버튼 비활성화
        self.monster_btn_active(False)

        # 공격 버튼 비활성화
        getattr(self, f'Status{self.user_turn}_Action1_Attack').setEnabled(False)

        print(f'다음 턴으로 넘어가야됨=========================(지금 유저턴{self.user_turn})')
        # self.go_to_normalfield()

        if self.user_turn == 5:
            self.user_turn = 0  # 유저 턴 0으로 만들어주고 다른 버튼들 비활성화 시켜줌(나중에 단축시킬 것)
            self.set_actions_enabled(1, False)  # 비활성화 시켜주고
            self.set_actions_enabled(2, False)  # 비활성화 시켜주고
            self.set_actions_enabled(3, False)  # 비활성화 시켜주고
            self.set_actions_enabled(4, False)  # 비활성화 시켜주고
            self.set_actions_enabled(5, False)  # 비활성화 시켜주고
            # if all(h == 0 for h in self.class_hp_dict.values()):
            #     print("유저체력 모두 0")
            ### 몬스터 공격 함수로 넘어가야됨
            self.monster_attack_users()

        else:  # 유저턴이 5 미만이면 다시 유저턴으로 돌아감
            ################################### 다음 턴으로 넘어가기 몬스터 턴에서 더해주기!!!!!!!!!!!! ########################################
            self.User_Turn()

    def monster_attack_users(self):
        """몬스터가 유저 랜덤으로 때리는 함수"""
        # 살아있는 몬스터가 돌아가면서 랜덤으로 유저 때림
        # 유저hp가 0이 되면 패스
        # 살아있는 몬스터 수 세기(죽으면 hide() 시켜줌)

        self.alive_monster = []  # 살아있는 몬스터 리스트에 담아주기
        for i, j in self.monster_hp_dict.items():  # 몬스터 체력 딕셔너리는 몬스터 호출 함수 Add_Monster_info 에 있음. 여기서 체력을 가져와줌
            print(i, j)  # 확인용
            if j > 0:  # 만약 몬스터 체력이 0 이상이면
                self.alive_monster.append(i)  # 빈 리스트에 더해준다.
                pass
            elif j == 0:  # 만약 몬스터 체력이 0 이면
                pass
            else:  # 만약 몬스터 체력이 0 미만이면
                print("패스")
                pass

        print('살아있는 몬스터 리스트는', self.alive_monster)

        # 살아있는 클래스 수 세기
        self.alive_class = [key for key, value in self.class_hp_dict.items() if value > 0]


        # 어떤 클래스 때릴지 랜덤으로 리스트에 추가 - 몬스터 갯수만큼 세주기
        # 수정해서 미안하지만 리스트 6번을 공격 대상에서 빼야 했어서 어쩔 수 없었음
        attacked_class_list = []
        for i in range(1, len(self.alive_monster) + 1):
            attacked_class_list.append(random.choice(self.alive_class))
            while True:
                if attacked_class_list[-1] == 6:
                    del attacked_class_list[-1]
                    attacked_class_list.append(random.choice(self.alive_class))
                else:
                    break

        print("attacked_class_list", attacked_class_list)

        # 클래스의 hp 깎아준다

        class_hp_present_value_list = [  # 클래스 값 넣어줄 리스트
            self.Status1_2_HpValue,
            self.Status2_2_HpValue,
            self.Status3_2_HpValue,
            self.Status4_2_HpValue,
            self.Status5_2_HpValue,
        ]
        death_class = []
        for m in range(1, len(self.alive_monster) + 1):
            self.Log_textEdit.append(f"{m}번째 몬스터가 {attacked_class_list[m - 1]}번 클래스를 100만큼 때립니다...")
            print(f"{m}번째 몬스터가 {attacked_class_list[m - 1]}번 클래스를 100만큼 때립니다...")
            self.class_hp_dict[attacked_class_list[m - 1]] = self.class_hp_dict[attacked_class_list[m - 1]] - (
                    100 - int(getattr(self, f'Class{attacked_class_list[m - 1]}_DetailsStatus_ShieldValue').text()))     # 임시로 100씩 때린다 <- 방어력을 넣어 공격력 감쇄 추가해봄
            print(self.class_hp_dict)  # 확인용

            for i in range(1, 6):
                if self.class_hp_dict[i] <= 0:
                    if attacked_class_list[m - 1] not in death_class:
                        death_class.append(attacked_class_list[m - 1])
                        self.class_hp_dict[attacked_class_list[m - 1]] = 0
                        print('죽은 클래스는', death_class)
                        self.Log_textEdit.append(f"{attacked_class_list[m - 1]}번 클래스가 사망했습니다.")
                        print(f"{attacked_class_list[m - 1]}번 클래스가 사망했습니다.")
                    else:
                        self.class_hp_dict[attacked_class_list[m - 1]] = 0

        for i in range(1, 6):
            class_hp_present_value_list[i - 1].setText(
                f'{self.class_hp_dict[i]}/{self.Statusclass[i - 1].get_maxhp()}')  # hp판에 변경된 값 넣어주기

        print("몬스터 공격이 종료되었습니다.")
        self.status_page_reset()    #페이지 리셋 추가

        self.User_Turn()

    def monster_btn_active(self, state):
        """몬스터 버튼 활성화 함수"""
        for i in range(1, 11):
            getattr(self, f'Monster_{i}_QButton').setEnabled(state)
        # Monster_1_QButton

    def active_class_frame(self, index):
        """특정 클래스 프레임 활성화 """
        print('가져온 인덱스는', index)
        for num in range(1, 6):
            if num == index:
                getattr(self, f'Status{num}_Action1_Attack').setEnabled(True)
                getattr(self, f'Status{num}_Action2_Skill').setEnabled(True)
                getattr(self, f'Status{num}_Action3_Item').setEnabled(True)
                getattr(self, f'Status{num}_Action4_Run').setEnabled(True)
            else:
                getattr(self, f'Status{num}_Action1_Attack').setEnabled(False)
                getattr(self, f'Status{num}_Action2_Skill').setEnabled(False)
                getattr(self, f'Status{num}_Action3_Item').setEnabled(False)
                getattr(self, f'Status{num}_Action4_Run').setEnabled(False)

    def set_actions_enabled(self, status_count, enabled):
        """클래스 프레임 활성화/비활성화 시키기"""
        for i in range(1, status_count + 1):
            getattr(self, f'Status{i}_Action1_Attack').setEnabled(enabled)
            getattr(self, f'Status{i}_Action2_Skill').setEnabled(enabled)
            getattr(self, f'Status{i}_Action3_Item').setEnabled(enabled)
            getattr(self, f'Status{i}_Action4_Run').setEnabled(enabled)

    def keyPressEvent(self, event):

        # 소연 keypressevent 함수 내 수정(current_index값 받아오기)===========================================================

        # 현재 스택위젯 값 가져오기
        current_index = self.StackWidget_Field.currentIndex()

        ## 일반필드일 때
        if current_index == 0:
            # 움직이는 {라벨} 현재 위치 정보 가져옴 <= 이전위치
            previous_position = self.Character_QLabel.geometry()

            rand_event = random.randrange(1, 11)
            if ((event.key() == Qt.Key_A)  # "a"키를 누를경우 캐릭터 현재 x값을 -20
                    and (self.Character_QLabel.x() > 0)):
                self.Character_QLabel.setPixmap(self.character_left_img)
                self.Character_QLabel.move(self.Character_QLabel.x() - 20, self.Character_QLabel.y())

            elif ((event.key() == Qt.Key_D)  # "d"키를 누를경우 캐릭터 현재 x값을 +20
                  and (self.Character_QLabel.x() < 1560)):
                self.Character_QLabel.setPixmap(self.character_right_img)
                self.Character_QLabel.move(self.Character_QLabel.x() + 20, self.Character_QLabel.y())

            elif ((event.key() == Qt.Key_W)  # "w"키를 누를경우 캐릭터 현재 y값을 -20
                  and (self.Character_QLabel.y() > -20)):
                self.Character_QLabel.move(self.Character_QLabel.x(), self.Character_QLabel.y() - 20)

            elif ((event.key() == Qt.Key_S)  # "s"키를 누를경우 캐릭터 현재 y값을 +20
                  and (self.Character_QLabel.y() < 740)):
                self.Character_QLabel.move(self.Character_QLabel.x(), self.Character_QLabel.y() + 20)

            else:  # 방향키 이외의 키를 눌렀을때를 위한 예외처리
                return

            self.lab_x_ = self.Character_QLabel.pos().x()  # 캐릭터의 현재 x값을 구한 후 lab_x_변수에 담음
            self.lab_y_ = self.Character_QLabel.pos().y()  # 캐릭터의 현재 y값을 구한 후 lab_y_변수에 담음

            if ((self.Character_QLabel.x() >= 0)  # 캐릭터가 다음칸으로 이동했을때 나오는 분기점 및 예외처리
                    and (self.Character_QLabel.x() <= 1580)
                    and (self.Character_QLabel.y() >= 0)
                    and (self.Character_QLabel.y() <= 780)):
                # 확률 33.33%
                if rand_event <= 5:
                    self.Log_textEdit.append("1칸 이동하였습니다.")


                elif rand_event <= 7:
                    self.HoldSwitch = 1  # 스택 위젯 페이지 이동후에도 캐릭터 이동하는 현상 예외처리
                    enemy_rand = random.randrange(4)
                    if enemy_rand < 3:
                        self.Log_textEdit.setText("적을 만났습니다.")
                        self.StackWidget_Field.setCurrentIndex(2)  # 전투필드로 이동
                        self.Add_Monster_info()
                        self.User_Turn()
                        """
                        적을 만났을때 설정값
                        """
                        # 인벤토리 ui를 소비창으로 변경
                        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
                        self.Page_Use.setEnabled(False)

                    else:
                        self.Log_textEdit.append("타 수호대를 만났습니다.")


                elif rand_event > 7:
                    tent_rate = random.randint(1, 100)
                    if tent_rate < 10:
                        self.item_list[10].stack += 1
                        self.Log_textEdit.append("%s 를 획득하였습니다."
                                                 % self.item_list[10].name)
                        self.consumable_reset()
                    elif self.guardLevel <= 20:
                        self.item_list[0].stack += 1
                        self.item_list[3].stack += 1
                        self.Log_textEdit.append("%s ,%s 를 획득하였습니다."
                                                 % (self.item_list[0].name, self.item_list[3].name))
                        self.consumable_reset()
                    elif 20 < self.guardLevel <= 40:
                        self.item_list[1].stack += 1
                        self.item_list[4].stack += 1
                        self.Log_textEdit.append("%s ,%s 를 획득하였습니다."
                                                 % (self.item_list[1].name, self.item_list[4].name))
                        self.consumable_reset()
                    elif 40 < self.guardLevel <= 60:
                        self.item_list[2].stack += 1
                        self.item_list[5].stack += 1
                        self.Log_textEdit.append("%s ,%s 를 획득하였습니다."
                                                 % (self.item_list[2].name, self.item_list[5].name))
                        self.consumable_reset()
                    elif 60 < self.guardLevel <= 70:
                        self.item_list[6].stack += 1
                        self.Log_textEdit.append("%s 를 획득하였습니다."
                                                 % self.item_list[6].name)
                        self.consumable_reset()
                    elif 70 < self.guardLevel <= 80:
                        self.item_list[7].stack += 1
                        self.Log_textEdit.append("%s 를 획득하였습니다."
                                                 % self.item_list[7].name)
                        self.consumable_reset()
                    else:
                        self.item_list[8].stack += 1
                        self.Log_textEdit.append("%s 를 획득하였습니다."
                                                 % self.item_list[8].name)
                        self.consumable_reset()
            # 왼쪽 상단에 변경된 죄표 값 출력
            self.TopUI_Coordinate_Label.setText(f"x좌표: {self.lab_x_} y좌표: {self.lab_y_}")
            self.TopUI_Map_Label.setText("%s의 지역" % self.user_location(self.lab_x_, self.lab_y_))

        ## 던전필드일때
        elif current_index == 1:
            pass
        else:
            return
    def user_location(self, x, y):
        """유저의 위치값 반환함"""
        user_present_location = {
            '불': [0, 760, -20, 360],  # 불의지역 x1, x2, y3, y4  값
            '눈': [780, 1560, -20, 360],  # 눈의지역
            '숲': [0, 760, 380, 740],  # 숲의지역
            '물': [780, 1560, 380, 740]  # 물의지역
        }

        for key, value in user_present_location.items():

            if value[0] <= x <= value[1] and value[2] <= y <= value[3]:
                return key
    """길준이 형님 코드 취합 - 함수"""
    def hp_using_1(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.hp_recovery_1(y))

        # self.Class_1_Btn.clicked.connect(lambda: self.hp_recovery_1(1))
        # self.Class_2_Btn.clicked.connect(lambda: self.hp_recovery_1(2))
        # self.Class_3_Btn.clicked.connect(lambda: self.hp_recovery_1(3))
        # self.Class_4_Btn.clicked.connect(lambda: self.hp_recovery_1(4))
        # self.Class_5_Btn.clicked.connect(lambda: self.hp_recovery_1(5))
        # self.Class_6_Btn.clicked.connect(lambda: self.hp_recovery_1(6))

    def hp_using_2(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.hp_recovery_2(y))

    def hp_using_3(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.hp_recovery_3(y))

    def mp_using_1(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.mp_recovery_1(y))

    def mp_using_2(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.mp_recovery_2(y))

    def mp_using_3(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.mp_recovery_3(y))

    def all_using_1(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.all_recovery_1(y))

    def all_using_2(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.all_recovery_2(y))

    def all_using_3(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.all_recovery_3(y))

    def revive_using(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.revive(y))

    # def tent_use_using(self):
    #     self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
    #     for i in range(1, 7):
    #         getattr(self, f'Class_{i}_Btn').setEnabled(True)
    #     for j in range(1, 7):
    #         getattr(self, f'Class_{j}_Btn').clicked.connect(lambda: self.tent_use(j))

    def class_change_using(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(0, 5):
            getattr(self, f'Class_{i+1}_Btn').setEnabled(True)
        self.Class_6_Btn.setEnabled(False)
        for j in range(1, 6):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.class_change(y))

    def hp_recovery_1(self, num):
        before = self.class_hp_dict[num]
        self.class_hp_dict[num] = self.class_hp_dict[num] + self.hp_s.recovery
        after = self.class_hp_dict[num]
        # str(self.list_class[i - 1][0].get_maxhp())
        # self.list_class[i - 1][1]
        if before < self.list_class[num - 1][0].get_maxhp() <= after:
            self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
            self.Log_textEdit.append("%s 의 체력을 최대치까지 회복했습니다"
                                     % getattr(self, f'class_{num}').character_name)
            self.item_list[0].stack -= 1

        elif self.class_hp_dict[num] >= self.list_class[num - 1][0].get_maxhp():
            self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
            self.Log_textEdit.append('이미 체력이 최대치입니다')

        else:
            self.Log_textEdit.append("%s 의 체력을 %s 만큼 회복했습니다" %
                                     (self.list_class[num - 1][0].character_name, self.hp_s.recovery))
            self.item_list[0].stack -= 1

        self.consumable_reset()

        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def hp_recovery_2(self, num):
        before = self.class_hp_dict[num]
        self.class_hp_dict[num] = self.class_hp_dict[num] + self.hp_m.recovery
        after = self.class_hp_dict[num]

        if before < self.list_class[num - 1][0].get_maxhp() <= after:
            self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
            self.Log_textEdit.append("%s 의 체력을 최대치까지 회복했습니다"
                                     % getattr(self, f'class_{num}').character_name)
            self.item_list[1].stack -= 1

        elif self.class_hp_dict[num] >= self.list_class[num - 1][0].get_maxhp():
            self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
            self.Log_textEdit.append('이미 체력이 최대치입니다')

        else:
            self.Log_textEdit.append("%s 의 체력을 %s 만큼 회복했습니다" %
                                     (self.list_class[num - 1][0].character_name, self.hp_m.recovery))
            self.item_list[1].stack -= 1

        self.consumable_reset()

        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def hp_recovery_3(self, num):
        before = self.class_hp_dict[num]
        self.class_hp_dict[num] = self.class_hp_dict[num] + self.hp_l.recovery
        after = self.class_hp_dict[num]

        if before < self.list_class[num - 1][0].get_maxhp() <= after:
            self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
            self.Log_textEdit.append("%s 의 체력을 최대치까지 회복했습니다"
                                     % getattr(self, f'class_{num}').character_name)
            self.item_list[2].stack -= 1

        elif self.class_hp_dict[num] >= self.list_class[num - 1][0].get_maxhp():
            self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
            self.Log_textEdit.append('이미 체력이 최대치입니다')

        else:
            self.Log_textEdit.append("%s 의 체력을 %s 만큼 회복했습니다" %
                                     (self.list_class[num - 1][0].character_name, self.hp_l.recovery))
            self.item_list[2].stack -= 1

        self.consumable_reset()

        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)

        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def mp_recovery_1(self, num):
        if getattr(self, f'class_{num}').class_name == '전사':
            self.Log_textEdit.append("전사는 회복시킬 마나가 없습니다")
            pass
        else:
            before = self.class_mp_dict[num]
            self.class_mp_dict[num] = self.class_mp_dict[num] + self.mp_s.recovery
            after = self.class_mp_dict[num]

            if before < self.list_class[num - 1][0].get_maxmp() <= after:
                self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
                self.Log_textEdit.append("%s 의 마나를 최대치까지 회복했습니다"
                                         % getattr(self, f'class_{num}').character_name)
                self.item_list[3].stack -= 1

            elif self.class_mp_dict[num] >= self.list_class[num - 1][0].get_maxmp():
                self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
                self.Log_textEdit.append('이미 마나가 최대치입니다')
                pass

            else:
                self.Log_textEdit.append("%s 의 마나를 %s 만큼 회복했습니다" % (
                    getattr(self, f'class_{num}').character_name, self.mp_s.recovery))
                self.item_list[3].stack -= 1

        self.consumable_reset()

        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def mp_recovery_2(self, num):
        if getattr(self, f'class_{num}').class_name == '전사':
            self.Log_textEdit.append("전사는 회복시킬 마나가 없습니다")
            pass
        else:
            before = self.class_mp_dict[num]
            self.class_mp_dict[num] = self.class_mp_dict[num] + self.mp_m.recovery
            after = self.class_mp_dict[num]

            if before < self.list_class[num - 1][0].get_maxmp() <= after:
                self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
                self.Log_textEdit.append("%s 의 마나를 최대치까지 회복했습니다"
                                         % getattr(self, f'class_{num}').character_name)
                self.item_list[4].stack -= 1

            elif self.class_mp_dict[num] >= self.list_class[num - 1][0].get_maxmp():
                self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
                self.Log_textEdit.append('이미 마나가 최대치입니다')
                pass

            else:
                self.Log_textEdit.append("%s 의 마나를 %s 만큼 회복했습니다" % (
                    getattr(self, f'class_{num}').character_name, self.mp_m.recovery))
                self.item_list[4].stack -= 1

        self.consumable_reset()
        self.low_ui_reset()
        self.status_page_reset()

        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def mp_recovery_3(self, num):
        if getattr(self, f'class_{num}').class_name == '전사':
            self.Log_textEdit.append("전사는 회복시킬 마나가 없습니다")
            pass
        else:
            before = self.class_mp_dict[num]
            self.class_mp_dict[num] = self.class_mp_dict[num] + self.mp_l.recovery
            after = self.class_mp_dict[num]

            if before < self.list_class[num - 1][0].get_maxmp() <= after:
                self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
                self.Log_textEdit.append("%s 의 마나를 최대치까지 회복했습니다"
                                         % getattr(self, f'class_{num}').character_name)
                self.item_list[5].stack -= 1

            elif self.class_mp_dict[num] >= self.list_class[num - 1][0].get_maxmp():
                self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
                self.Log_textEdit.append('이미 마나가 최대치입니다')
                pass

            else:
                self.Log_textEdit.append("%s 의 마나를 %s 만큼 회복했습니다" % (
                    getattr(self, f'class_{num}').character_name, self.mp_l.recovery))
                self.item_list[5].stack -= 1

        self.consumable_reset()

        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def all_recovery_1(self, num):
        # getattr(self, f'class_{num}').hp = getattr(self, f'class_{num}').hp + ((체력 최대치) * self.all_s.recovery)
        # if getattr(self, f'class_{num}').hp > (체력 최대치)
        #     getattr(self, f'class_{num}').hp = (체력 최대치)
        # getattr(self, f'class_{num}').mp = getattr(self, f'class_{num}').mp + ((마나 최대치) * self.all_s.recovery)
        # if getattr(self, f'class_{num}').mp > (마나 최대치)
        #     getattr(self, f'class_{num}').mp = (마나 최대치)

        before_hp = self.class_hp_dict[num]
        self.class_hp_dict[num] = self.class_hp_dict[num] + int(
                self.list_class[num - 1][0].get_maxhp() * self.all_s.recovery)
        after_hp = self.class_hp_dict[num]
        before_mp = self.class_mp_dict[num]
        self.class_mp_dict[num] = self.list_class[num - 1][2] + int(
                self.list_class[num - 1][0].get_maxmp() * self.all_s.recovery)
        after_mp = self.class_mp_dict[num]

        if self.class_hp_dict[num] >= self.list_class[num - 1][0].get_maxhp() \
                and self.class_mp_dict[num] >= self.list_class[num - 1][0].get_maxmp():
            self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
            self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
            self.Log_textEdit.append('이미 체력과 마나가 최대치입니다')
            pass

        else:
            if before_hp < self.list_class[num - 1][0].get_maxhp() <= after_hp:
                self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
                self.Log_textEdit.append("%s 의 체력을 최대치까지 회복했습니다"
                                         % getattr(self, f'class_{num}').character_name)

            else:
                self.Log_textEdit.append("%s 의 체력를 %s %% 만큼 회복했습니다" % (
                    getattr(self, f'class_{num}').character_name, self.all_s.recovery*100))

            if before_mp < self.list_class[num - 1][0].get_maxmp() <= after_mp:
                self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
                self.Log_textEdit.append("%s 의 마나를 최대치까지 회복했습니다"
                                         % getattr(self, f'class_{num}').character_name)

            else:
                self.Log_textEdit.append("%s 의 마나를 %s %% 만큼 회복했습니다" % (
                    getattr(self, f'class_{num}').character_name, self.all_s.recovery * 100))

            self.item_list[6].stack -= 1

        self.consumable_reset()

        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def all_recovery_2(self, num):
        # getattr(self, f'class_{num}').hp = getattr(self, f'class_{num}').hp + ((체력 최대치) * self.all_m.recovery)
        # if getattr(self, f'class_{num}').hp > (체력 최대치)
        #     getattr(self, f'class_{num}').hp = (체력 최대치)
        # getattr(self, f'class_{num}').mp = getattr(self, f'class_{num}').mp + ((마나 최대치) * self.all_m.recovery)
        # if getattr(self, f'class_{num}').mp > (마나 최대치)
        #     getattr(self, f'class_{num}').mp = (마나 최대치)
        before_hp = self.list_class[num - 1][1]
        self.list_class[num - 1][1] = self.list_class[num - 1][1] + (
                self.list_class[num - 1][0].get_maxhp() * self.all_m.recovery)
        after_hp = self.list_class[num - 1][1]
        before_mp = self.list_class[num - 1][2]
        self.list_class[num - 1][2] = self.list_class[num - 1][2] + (
                self.list_class[num - 1][0].get_maxmp() * self.all_m.recovery)
        after_mp = self.list_class[num - 1][2]

        if self.list_class[num - 1][1] >= self.list_class[num - 1][0].get_maxhp() \
                and self.list_class[num - 1][2] >= self.list_class[num - 1][0].get_maxmp():
            self.list_class[num - 1][1] = self.list_class[num - 1][0].get_maxhp()
            self.list_class[num - 1][2] = self.list_class[num - 1][0].get_maxmp()
            self.Log_textEdit.append('이미 체력과 마나가 최대치입니다')
            pass

        if before_hp < self.list_class[num - 1][0].get_maxhp() <= after_hp:
            self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
            self.Log_textEdit.append("%s 의 체력을 최대치까지 회복했습니다"
                                      % getattr(self, f'class_{num}').character_name)

        else:
            self.Log_textEdit.append("%s 의 체력를 %s %% 만큼 회복했습니다" % (
                getattr(self, f'class_{num}').character_name, self.all_s.recovery * 100))

        if before_mp < self.list_class[num - 1][0].get_maxmp() <= after_mp:
            self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
            self.Log_textEdit.append("%s 의 마나를 최대치까지 회복했습니다"
                                     % getattr(self, f'class_{num}').character_name)
        else:
            self.Log_textEdit.append("%s 의 마나를 %s %% 만큼 회복했습니다" % (
            getattr(self, f'class_{num}').character_name, self.all_s.recovery * 100))

        self.item_list[7].stack -= 1
        self.consumable_reset()

        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def all_recovery_3(self, num):
        if self.class_hp_dict[num] >= self.list_class[num - 1][0].get_maxhp() \
                and self.class_mp_dict[num] >= self.list_class[num - 1][0].get_maxmp():
            self.Log_textEdit.append('이미 체력과 마나가 최대치입니다')
            pass
        else:
            self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
            self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
            self.Log_textEdit.append("체력과 마나를 전부 회복했습니다")

        self.item_list[8].stack -= 1
        self.consumable_reset()

        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def revive(self, num):
        # getattr(self, f'class_{num}').hp = (체력 최대치)
        # getattr(self, f'class_{num}').mp = (마나 최대치)
        self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
        self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
        self.Log_textEdit.append("체력과 마나를 전부 회복했습니다")

        self.item_list[9].stack -= 1
        self.consumable_reset()

        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()
        # '선택된' 캐릭터 전투불능 해제

    def tent_use(self):
        self.item_list[10].stack -= 1
        # for i in range(1, 7):
        # getattr(self, f'class_{i}').hp = getattr(self, f'class_{i}').hp (최대치)
        # for j in range(1, 7):
        # getattr(self, f'class_{j}').mp = getattr(self, f'class_{j}').mp (최대치)
        # '모든' 캐릭터 전투불능 해제
        for i in range(len(self.class_hp_dict)):
            self.class_hp_dict[i] = self.list_class[i - 1][0].get_maxhp()
            self.class_mp_dict[i] = self.list_class[i - 1][0].get_maxmp()
        self.Log_textEdit.append("체력과 마나를 전부 회복했습니다")
        self.consumable_reset()
        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        for k in range(1, 7):
            getattr(self, f'Class_{k}_Btn').disconnect()

    def class_change(self, num):
        # 1-6

        self.Log_textEdit.append('%s이/가 후퇴하고 %s이/가 출전하였습니다.'
                                 % (self.list_class[num-1][0].character_name, self.list_class[-1][0].character_name))
        self.ComboBox_Class.clear()  # 콤보박스 리스트 전부 제거
        go_battle = self.list_class.pop(-1)  # 대기중인 캐릭터를 이름 리스트에서 추출
        out_battle = self.list_class.pop(num-1)  # 빠질 캐릭터를 이름 리스트에서 추출
        self.list_class.insert(num-1, go_battle)  # 들어갈 캐릭터를 빠진 캐릭터 위치로 이동
        self.list_class.append(out_battle)  # 빠질 캐릭터를 대기 위치로 이동
        self.class_hp_dict.clear()
        self.class_mp_dict.clear()
        for i in range(1, 7):  # 서플로 돌려준 클래스유저들의 체력을 빈 딕셔너리에 1부터 6까지 담아줌 <- 수정함
            self.class_hp_dict[i] = self.list_class[i - 1][1]
        for i in range(1, 7):  # 서플로 돌려준 클래스유저들의 마나를 빈 딕셔너리에 1부터 6까지 담아줌 <- 수정함
            self.class_mp_dict[i] = self.list_class[i - 1][2]
        self.Statusclass.clear()
        self.StautsHpall.clear()
        self.StautsMpall.clear()
        print('유저 체력 확인용', self.class_hp_dict)

        # 위에서 섞은 list_class을 프레임에 1부터 5까지 가져와 담아줌
        for i in range(1, 6):
            # 빈 리스트에 추가
            self.Statusclass.append(self.list_class[i - 1][0])  # 빈 리스트 Statusclass에 하나씩 전체정보를 append해줌
            self.StautsHpall.append(self.list_class[i - 1][1])  # 빈 리스트 StautsHpall에 하나씩 최대hp를 append해줌
            self.StautsMpall.append(self.list_class[i - 1][1])  # 빈 리스트 StautsMpall에 하나씩 최대mp를 append해줌

        self.class_equip_page()
        self.class_name_reset()
        self.low_ui_reset()
        self.item_list[11].stack -= 1
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        self.consumable_reset()
        self.combobox_add()  # 콤보박스를 리스트 대로 재작성
        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        for i in range(1, 6):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def combobox_add(self):
        self.ComboBox_Class.addItem(self.list_class[0][0].character_name)
        self.ComboBox_Class.addItem(self.list_class[1][0].character_name)
        self.ComboBox_Class.addItem(self.list_class[2][0].character_name)
        self.ComboBox_Class.addItem(self.list_class[3][0].character_name)
        self.ComboBox_Class.addItem(self.list_class[4][0].character_name)
        self.ComboBox_Class.setCurrentIndex(0)

    def helmet_upgrade(self):

        item_name_before = getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name
        upgrade_rate = random.randint(1, 100)

        if getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[0] == 0 and upgrade_rate < 4:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[0] = head_list[1]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[0] = head_list[4]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name.find('철') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[0] = head_list[7]
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[0] = 1
            self.item_list[-2].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[0] == 1 and upgrade_rate < 2:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[0] = head_list[2]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[0] = head_list[5]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name.find('철') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[0] = head_list[8]
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[0] = 2
            self.item_list[-1].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[0] == 0:
            self.item_list[-2].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[0] == 1:
            self.item_list[-1].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        self.consumable_reset()
        self.item_upgrade_button_reset()

    def armor_upgrade(self):

        item_name_before = getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name
        upgrade_rate = random.randint(1, 100)

        if getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[1] == 0 and upgrade_rate < 4:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1] = armor_list[1]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1] = armor_list[4]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('중') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1] = armor_list[7]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('경') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1] = armor_list[10]
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[1] = 1
            self.item_list[-2].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[1] == 1 and upgrade_rate < 2:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1] = armor_list[2]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1] = armor_list[5]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('철') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1] = armor_list[8]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('경') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1] = armor_list[11]
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[1] = 2
            self.item_list[-1].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[1] == 0:
            self.item_list[-2].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[1] == 1:
            self.item_list[-1].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        self.consumable_reset()
        self.item_upgrade_button_reset()

    def pants_upgrade(self):
        item_name_before = getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name
        upgrade_rate = random.randint(1, 100)
        if getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[2] == 0 and upgrade_rate < 4:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[2] = pants_list[1]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[2] = pants_list[4]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name.find('중') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[2] = pants_list[7]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name.find('경') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[2] = pants_list[10]
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[2] = 1
            self.item_list[-2].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[2] == 1 and upgrade_rate < 2:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[2] = pants_list[2]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[2] = pants_list[5]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name.find('철') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[2] = pants_list[8]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name.find('경') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[2] = pants_list[11]
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[2] = 2
            self.item_list[-1].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[2] == 0:
            self.item_list[-2].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[2] == 1:
            self.item_list[-1].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        self.consumable_reset()
        self.item_upgrade_button_reset()

    def glove_upgrade(self):
        item_name_before = getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name
        upgrade_rate = random.randint(1, 100)

        if getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[3] == 0 and upgrade_rate < 4:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[3] = glove_list[1]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[3] = glove_list[4]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name.find('사슬') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[3] = glove_list[7]
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[3] = 1
            self.item_list[-2].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))
        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[3] == 1 and upgrade_rate < 2:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[3] = glove_list[2]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[3] = glove_list[5]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name.find('사슬') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[3] = glove_list[8]
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[3] = 2
            self.item_list[-1].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[3] == 0:
            self.item_list[-2].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[3] == 1:
            self.item_list[-1].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        self.consumable_reset()
        self.item_upgrade_button_reset()

    def weapon_upgrade(self):
        item_name_before = getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name
        upgrade_rate = random.randint(1, 100)
        if getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[4] == 0 and upgrade_rate < 4:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('검') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = weapon_list[1]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('숏') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = weapon_list[7]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('롱') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = weapon_list[10]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('룬') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = weapon_list[13]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('보우') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = weapon_list[16]
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[4] = 1
            self.item_list[-2].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))
        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[4] == 1 and upgrade_rate < 2:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('검') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = weapon_list[2]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('숏') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = weapon_list[8]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('롱') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = weapon_list[11]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('룬') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = weapon_list[14]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('보우') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = weapon_list[17]
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[4] = 2
            self.item_list[-1].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))
        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[4] == 0:
            self.item_list[-2].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[4] == 1:
            self.item_list[-1].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)
        self.consumable_reset()
        self.item_upgrade_button_reset()

    def shield_upgrade(self):
        item_name_before = getattr(self, f'item_class_{self.upgrade_index + 1}')[5].name
        upgrade_rate = random.randint(1, 100)

        if getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[5] == 0 and upgrade_rate < 4:
            getattr(self, f'item_class_{self.upgrade_index + 1}')[5] = weapon_list[4]
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[5] = 1
            self.item_list[-2].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[5].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[5] == 1 and \
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('중') != -1 and upgrade_rate < 2:
            getattr(self, f'item_class_{self.upgrade_index + 1}')[5] = weapon_list[5]
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[5] = 2
            self.item_list[-1].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[5].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[5] == 0:
            self.item_list[-2].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[5] == 1:
            self.item_list[-1].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        self.consumable_reset()
        self.item_upgrade_button_reset()

    def cloak_upgrade(self):
        item_name_before = getattr(self, f'item_class_{self.upgrade_index + 1}')[6].name
        upgrade_rate = random.randint(1, 100)
        if getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[6] == 0 and upgrade_rate < 4:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[6].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[6] = cloak_list[1]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[6].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[6] = cloak_list[4]
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[6] = 1
            self.item_list[-2].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[6].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))
        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[6] == 1 and upgrade_rate < 2:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[6].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[6] = cloak_list[2]
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[6].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[6] = cloak_list[5]
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[6] = 2
            self.item_list[-1].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[6].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))
        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[6] == 0:
            self.item_list[-2].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[6] == 1:
            self.item_list[-1].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)
        self.consumable_reset()
        self.item_upgrade_button_reset()

    def class_name_reset(self):
        self.list_class_name = [self.list_class[0][0].character_name, self.list_class[1][0].character_name,
                                self.list_class[2][0].character_name, self.list_class[3][0].character_name,
                                self.list_class[4][0].character_name, self.list_class[5][0].character_name]

    def item_upgrade_button_reset(self):
        for i in range(0, 6):
            if self.item_list[-2].stack > 0 or self.item_list[-1].stack > 0:
                getattr(self, f'Equip{i + 1}_1Helmet_Btn').setEnabled(True)
            if self.item_list[-2].stack > 0 or self.item_list[-1].stack > 0:
                getattr(self, f'Equip{i + 1}_2_Armor_Btn').setEnabled(True)
            if self.item_list[-2].stack > 0 or self.item_list[-1].stack > 0:
                getattr(self, f'Equip{i + 1}_3_Pants_Btn').setEnabled(True)
            if self.item_list[-2].stack > 0 or self.item_list[-1].stack > 0:
                getattr(self, f'Equip{i + 1}_5_Hand_Btn').setEnabled(True)
            if self.item_list[-2].stack > 0 or self.item_list[-1].stack > 0:
                getattr(self, f'Equip{i + 1}_6_Weapon_Btn').setEnabled(True)
            if self.item_list[-2].stack > 0 or self.item_list[-1].stack > 0:
                getattr(self, f'Equip{i + 1}_7_Shield_Btn').setEnabled(True)
            if self.item_list[-2].stack > 0 or self.item_list[-1].stack > 0:
                getattr(self, f'Equip{i + 1}_8_Cloak_Btn').setEnabled(True)

            if self.item_list[-2].stack == 0 or \
                    (self.item_list[-1].stack == 0 and getattr(self, f'item_class_upgrade_counter_{i + 1}')[
                        0] == 1):
                getattr(self, f'Equip{i + 1}_1Helmet_Btn').setEnabled(False)
            if self.item_list[-2].stack == 0 or \
                    (self.item_list[-1].stack == 0 and getattr(self, f'item_class_upgrade_counter_{i + 1}')[
                        1] == 1):
                getattr(self, f'Equip{i + 1}_2_Armor_Btn').setEnabled(False)
            if self.item_list[-2].stack == 0 or \
                    self.item_list[-1].stack == 0 and getattr(self, f'item_class_upgrade_counter_{i + 1}')[2] == 1:
                getattr(self, f'Equip{i + 1}_3_Pants_Btn').setEnabled(False)
            if self.item_list[-2].stack == 0 or \
                    self.item_list[-1].stack == 0 and getattr(self, f'item_class_upgrade_counter_{i + 1}')[3] == 1:
                getattr(self, f'Equip{i + 1}_5_Hand_Btn').setEnabled(False)
            if self.item_list[-2].stack == 0 or \
                    self.item_list[-1].stack == 0 and getattr(self, f'item_class_upgrade_counter_{i + 1}')[4] == 1:
                getattr(self, f'Equip{i + 1}_6_Weapon_Btn').setEnabled(False)
            if self.item_list[-2].stack == 0 or \
                    self.item_list[-1].stack == 0 and getattr(self, f'item_class_upgrade_counter_{i + 1}')[5] == 1:
                getattr(self, f'Equip{i + 1}_7_Shield_Btn').setEnabled(False)
            if self.item_list[-2].stack == 0 or \
                    self.item_list[-1].stack == 0 and getattr(self, f'item_class_upgrade_counter_{i + 1}')[6] == 1:
                getattr(self, f'Equip{i + 1}_8_Cloak_Btn').setEnabled(False)

            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[0] == 2:
                getattr(self, f'Equip{i + 1}_1Helmet_Btn').setEnabled(False)
            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[1] == 2:
                getattr(self, f'Equip{i + 1}_2_Armor_Btn').setEnabled(False)
            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[2] == 2:
                getattr(self, f'Equip{i + 1}_3_Pants_Btn').setEnabled(False)
            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[3] == 2:
                getattr(self, f'Equip{i + 1}_5_Hand_Btn').setEnabled(False)
            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[4] == 2:
                getattr(self, f'Equip{i + 1}_6_Weapon_Btn').setEnabled(False)
            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[5] == 1:
                getattr(self, f'Equip{i + 1}_7_Shield_Btn').setEnabled(False)
            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[5] == 1 and \
                    getattr(self, f'item_class_{i + 1}')[1].name.find('중') != -1:
                getattr(self, f'Equip{i + 1}_7_Shield_Btn').setEnabled(True)
            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[5] == 2:
                getattr(self, f'Equip{i + 1}_7_Shield_Btn').setEnabled(False)
            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[6] == 2:
                getattr(self, f'Equip{i + 1}_8_Cloak_Btn').setEnabled(False)

            if getattr(self, f'item_class_{i + 1}')[5] is None:
                getattr(self, f'Equip{i + 1}_7_Shield_Btn').setEnabled(False)
            if getattr(self, f'item_class_{i + 1}')[1].name.find('천') != -1:
                getattr(self, f'Equip{i + 1}_7_Shield_Btn').setEnabled(False)

    def class_equip_page(self):
        self.character_selection = self.ComboBox_Class.currentText()
        if self.character_selection == '미하일':
            self.StackWidget_Equip.setCurrentWidget(self.Class_1_Equip_Page)
        elif self.character_selection == '루미너스':
            self.StackWidget_Equip.setCurrentWidget(self.Class_2_Equip_Page)
        elif self.character_selection == '알렉스':
            self.StackWidget_Equip.setCurrentWidget(self.Class_3_Equip_Page)
        elif self.character_selection == '샐러맨더':
            self.StackWidget_Equip.setCurrentWidget(self.Class_4_Equip_Page)
        elif self.character_selection == '메르데스':
            self.StackWidget_Equip.setCurrentWidget(self.Class_5_Equip_Page)
        elif self.character_selection == '랜슬롯':
            self.StackWidget_Equip.setCurrentWidget(self.Class_6_Equip_Page)



    def status_page_reset(self):
        for i in range(len(self.list_class)):
            # 0-6
            getattr(self, f'Class{i + 1}_DetailsStatus_Name').setText(self.list_class[i][0].character_name)
            getattr(self, f'Class{i + 1}_DetailsStatus_Class').setText(self.list_class[i][0].class_name)
            self.damage_status = str(self.class_item[i][4].damage * self.guardLevel)
            getattr(self, f'Class{i + 1}_DetailsStatus_AtkValue').setText(self.damage_status)
            if self.class_item[i][5] is None:
                defence_status = str((self.class_item[i][0].armor + self.class_item[i][1].armor +
                                      self.class_item[i][2].armor + self.class_item[i][3].armor +
                                      self.class_item[i][6].armor) * self.guardLevel)
            else:
                defence_status = str((self.class_item[i][0].armor + self.class_item[i][1].armor +
                                      self.class_item[i][2].armor + self.class_item[i][3].armor +
                                      self.class_item[i][5].damage + self.class_item[i][6].armor) * self.guardLevel)
            getattr(self, f'Class{i+1}_DetailsStatus_ShieldValue').setText(defence_status)

            getattr(self, f'Class{i + 1}_DetailsStatus_HpValue').setText(str(self.class_hp_dict.get(i+1)) +
                                                                         "/" + str(self.list_class[i][0].get_maxhp()))
            getattr(self, f'Class{i + 1}_DetailsStatus_MpValue').setText(str(self.class_mp_dict.get(i+1)) +
                                                                         "/" + str(self.list_class[i][0].get_maxmp()))
        # status_list = []
        # for mihail in range(len(self.list_class)):
        #     if self.list_class[mihail][0].character_name == '미하일':
        #         status_list.append(self.list_class[mihail])
        # for ruminus in range(len(self.list_class)):
        #     if self.list_class[ruminus][0].character_name == '루미너스':
        #         status_list.append(self.list_class[ruminus])
        # for alex in range(len(self.list_class)):
        #     if self.list_class[alex][0].character_name == '알렉스':
        #         status_list.append(self.list_class[alex])
        # for salamander in range(len(self.list_class)):
        #     if self.list_class[salamander][0].character_name == '샐러맨더':
        #         status_list.append(self.list_class[salamander])
        # for merdes in range(len(self.list_class)):
        #     if self.list_class[merdes][0].character_name == '메르데스':
        #         status_list.append(self.list_class[merdes])
        # for lancelot in range(len(self.list_class)):
        #     if self.list_class[lancelot][0].character_name == '랜슬롯':
        #         status_list.append(self.list_class[lancelot])



        # UI 오타 고칠때까지 작동 불가(해결)

        # 캐릭터 기본 공격력과 방어력 수치가 없음(해결)
        #     damage_status = str(self.class_item[i][4].damage * self.guardLevel)
        #     getattr(self, f'Class{i + 1}_DetailsStatus_AtkValue').setText(damage_status)
        #
        #     if self.class_item[i][5] is None:
        #         defence_status = str((self.class_item[i][0].armor + self.class_item[i][1].armor +
        #                              self.class_item[i][2].armor + self.class_item[i][3].armor +
        #                              self.class_item[i][6].armor) * self.guardLevel)
        #     else:
        #         defence_status = str((self.class_item[i][0].armor + self.class_item[i][1].armor +
        #                              self.class_item[i][2].armor + self.class_item[i][3].armor +
        #                              self.class_item[i][5].damage + self.class_item[i][6].armor) * self.guardLevel)
        #
        #     getattr(self, f'Class{i + 1}_DetailsStatus_ShieldValue').setText(defence_status)

        for o in range(len(self.list_class)-1):
            getattr(self, f'Class{o + 1}_DetailsStatus_ConditionValue').setText('출전중')
            self.Class6_DetailsStatus_ConditionValue.setText('휴식중')

    def low_ui_reset(self):
        for i in range(1, 6):
            # 하단 ui에 캐릭터 추가
            getattr(self, f'Status{i}_1_Class').setText(self.list_class[i - 1][0].class_name)  # 클래스명 지정
            getattr(self, f'Status{i}_1_Name').setText(self.list_class[i - 1][0].character_name)  # 캐릭터명 지정
            getattr(self, f'Status{i}_2_HpValue').setText(
                str(self.class_hp_dict.get(i)) + "/" + str(self.list_class[i - 1][0].get_maxhp()))  # hp(기본 값/변하는 값)
            getattr(self, f'Status{i}_3_MpValue').setText(
                str(self.class_mp_dict.get(i)) + "/" + str(self.list_class[i - 1][0].get_maxmp()))  # mp(기본 값/변하는 값)

            # 정렬 및 스타일시트 배경 디자인
            getattr(self, f'Status{i}_2_HpValue').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i}_1_Name').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i}_3_MpValue').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i}_1_Class').setAlignment(Qt.AlignCenter)  # 텍스트 가운데 정렬
            getattr(self, f'Status{i}_1_Class').setStyleSheet('QLabel{background-color:#55aaff;}')  # 클래스 배경 색상 지정
            getattr(self, f'Status{i}_2_Hp').setStyleSheet('QLabel{background-color:#55aaff;}')  # hp, mp 배경 색상 지정
            getattr(self, f'Status{i}_3_Mp').setStyleSheet('QLabel{background-color:#55aaff;}')

    def class_item_list(self):
        self.class_item = []
        for i in range(6):
            if self.list_class[i][0].class_name == '전사':
                self.class_item.append(class_warrior)
            elif self.list_class[i][0].class_name == '백법사':
                self.class_item.append(class_whitewizard)
            elif self.list_class[i][0].class_name == '흑법사':
                self.class_item.append(class_blackwizard)
            elif self.list_class[i][0].class_name == '적법사':
                self.class_item.append(class_redwizard)
            elif self.list_class[i][0].class_name == '궁수':
                self.class_item.append(class_archer)
            elif self.list_class[i][0].class_name == '검사':
                self.class_item.append(class_swordman)




    def get_index(self):
        self.upgrade_index = self.StackWidget_Equip.currentIndex()

    def consumable_reset(self):
        """소모품 갯수 갱신 함수"""
        for i in range(len(self.item_list) - 2):
            if self.item_list[i].stack > 0:
                getattr(self, f'Portion_{i + 1}_Btn').setEnabled(True)

        for i in range(len(self.item_list) - 2):
            if self.item_list[i].stack == 0:
                getattr(self, f'Portion_{i + 1}_Btn').setEnabled(False)

        for i in range(len(self.item_list)):
            getattr(self, f'Portion_{i + 1}_Value').display(self.item_list[i].stack)

    def use_page(self):
        self.Btn_Portion.setEnabled(False)
        self.Btn_Status.setEnabled(True)
        self.Btn_Equip.setEnabled(True)
        self.consumable_reset()

    def equip_page(self):
        self.Btn_Portion.setEnabled(True)
        self.Btn_Status.setEnabled(True)
        self.Btn_Equip.setEnabled(False)
        self.item_upgrade_button_reset()

    def status_page(self):
        self.Btn_Portion.setEnabled(True)
        self.Btn_Status.setEnabled(False)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(False)
        self.Btn_Equip.setEnabled(True)
        self.status_page_reset()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()