# version 0.0425.1
# tt 출력 추가
# processor 추가
# HRRN 수정
# 최대값 100으로 설정
version = '0.0425.1'

import sys
import os

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5 import uic
from PyQt5 import QtGui

from scheduleInfo import Process
from scheduleInfo import Request
from chartinfo import chartinfo
from HRRN import HRRN #
from SPN import SPN #
from RR import RR   # 김지우
from SRTN import SRTN # 박동주
from FCFS import FCFS # 김종현
from PSPN import PSPN

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form = resource_path('gui.ui')
form_class = uic.loadUiType(form)[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def initUI(self):
        self.setWindowIcon(QtGui.QIcon('1.png'))

    def __init__(self) :
        super().__init__()

        self.setupUi(self)
        self.initUI()
        self.setWindowTitle('Process Scheduler (' + version + ')')
        self.setFixedSize(1300, 850)
        # 802, 516
        self.centralWidget()
        #self.setWindowIcon(QIcon('web.png'))
        #self.setGeometry(300, 300, 300, 200)

        # image 넣기 (코룡이!)
        #qPixmapVar = QtGui.QPixmap()
        #qPixmapVar.load('1.png')
        #qPixmapVar.scaledToWidth(10)
        #qPixmapVar.scaledToWidth(self.label_image.width())
        #qPixmapVar.scaled(self.label_image.width(), self.label_image.height())
        #self.label_image.setPixmap(qPixmapVar)
        #print(self.label_image.width())

        # OS Algorithm에 필요한 변수
        self.request = Request()
        self.psList = []
        self.idList = set()
        self.tableItemList = []
        self.count = 0

        self.btn_push_enabled = False
        self.btn_start_enabled = False
        self.btn_reset_enabled = False
        self.input_priority_enabled = False

        # Chart 설정
        self.figure1 = plt.Figure(figsize=(6, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure1)

        self.chart_view.addWidget(self.canvas)

        # table 설정
        self.table_process.setRowCount(15)
        self.table_process.setColumnCount(8)
        self.table_process.setHorizontalHeaderLabels(['ID', 'AT', 'BT', 'Priority', 'WT', 'TT', 'NTT', ' '])
        self.table_process.setEditTriggers(QAbstractItemView.NoEditTriggers)

        column_width = self.table_process.width() - 30
        self.table_process.setColumnWidth(0, int(column_width * 11 / 100))
        self.table_process.setColumnWidth(1, int(column_width * 14 / 100))
        self.table_process.setColumnWidth(2, int(column_width * 14 / 100))
        self.table_process.setColumnWidth(3, int(column_width * 14 / 100))
        self.table_process.setColumnWidth(4, int(column_width * 14 / 100))
        self.table_process.setColumnWidth(5, int(column_width * 14 / 100))
        self.table_process.setColumnWidth(6, int(column_width * 14 / 100))
        self.table_process.setColumnWidth(7, int(column_width * 3 / 100)) # 1920 1080
        #self.table_process.setItem(0, 0, QTableWidgetItem("test"))

        for i in range(15):
            row = i
            column = 7
            button = QPushButton('x')
            button.setStyleSheet("background-color: rgb(255,88,88);"
                                 "color: white")
            self.table_process.setCellWidget(row, column, button)
            button.clicked.connect(
                lambda *args, row=row, column=column: self.command_delete(row, column))

        # Setting
        self.label_state_timeQuantum.setFont(QtGui.QFont("", 12))
        self.label_state_timeQuantum.setStyleSheet("Color : red")

        self.request.set_timeQuantum(2)
        self.request.set_coreNumber(1)
        self.input_timeQuantum.setText("2")

        self.input_timeQuantum.textChanged.connect(self.state_timeQuantum)

        self.btn_FCFS.clicked.connect(self.state_radioBtn)
        self.btn_RR.clicked.connect(self.state_radioBtn)
        self.btn_SPN.clicked.connect(self.state_radioBtn)
        self.btn_SRTN.clicked.connect(self.state_radioBtn)
        self.btn_HRRN.clicked.connect(self.state_radioBtn)
        self.btn_PSPN.clicked.connect(self.state_radioBtn)

        #self.slider_numOfProcessor.setValue(1)
        #self.slider_numOfProcessor.valueChanged.connect(self.state_coreNumber)


        # push(process input)
        self.input_id.setText("P1")
        self.label_state_process.setFont(QtGui.QFont("", 12))
        self.label_state_process.setStyleSheet("Color : red")

        self.input_id.textChanged.connect(self.state_push)
        self.input_at.textChanged.connect(self.state_push)
        self.input_bt.textChanged.connect(self.state_push)
        self.input_priority.textChanged.connect(self.state_push)
        self.input_id.returnPressed.connect(self.command_push)
        self.input_at.returnPressed.connect(self.command_push)
        self.input_bt.returnPressed.connect(self.command_push)
        self.input_priority.returnPressed.connect(self.command_push)
        self.btn_push.clicked.connect(self.command_push)
        self.btn_push.setEnabled(False)

        self.input_priority.setText('1')
        self.input_priority.setEnabled(False)

        # reset (process)
        self.btn_reset.clicked.connect(self.command_reset)
        self.btn_reset.setEnabled(False)

        # start
        self.btn_start.setEnabled(False)

        self.btn_start.clicked.connect(self.command_start)

        self.set_chart()

    # Table Setting
    def set_table_clear(self):
        for i in range(15):
            self.table_process.setItem(i, 0, QTableWidgetItem())
            self.table_process.setItem(i, 1, QTableWidgetItem())
            self.table_process.setItem(i, 2, QTableWidgetItem())
            self.table_process.setItem(i, 3, QTableWidgetItem())
            self.table_process.setItem(i, 4, QTableWidgetItem())
            self.table_process.setItem(i, 5, QTableWidgetItem())
            self.table_process.setItem(i, 6, QTableWidgetItem())

    def set_table(self):
        self.set_table_clear()
        # table view update
        for i in range(len(self.psList)):
            ps = self.psList[i]
            self.table_process.setItem(i, 0, QTableWidgetItem(str(ps.get_id())))
            self.table_process.setItem(i, 1, QTableWidgetItem(str(ps.get_at())))
            self.table_process.setItem(i, 2, QTableWidgetItem(str(ps.get_bt())))
            if self.input_priority_enabled:
                self.table_process.setItem(i, 3, QTableWidgetItem(str(ps.get_priority())))
            else :
                self.table_process.setItem(i, 3, QTableWidgetItem(str(1)))
            self.table_process.setItem(i, 4, QTableWidgetItem(str(round(ps.get_wt(), 4))))
            self.table_process.setItem(i, 5, QTableWidgetItem(str(round(ps.get_tt(), 4))))
            self.table_process.setItem(i, 6, QTableWidgetItem(str(round(ps.get_ntt(), 4))))

    def set_chart(self, val_return=[]):
        list_charts = val_return

        # 차트 상세
        self.figure1.clear()
        gnt = self.figure1.add_subplot(111)

        #gnt.set_xlabel('seconds since start')
        gnt.set_ylabel('Processor')
        gnt.set_ylim(0, 50)
        gnt.set_xlim(0, chartinfo.max_end_time + 1 + chartinfo.max_end_time // 5)
        gnt.set_yticks([10, 20, 30, 40])
        gnt.set_yticklabels(['1', '2', '3', '4'])

        gnt.set_xticks(np.arange(0, chartinfo.max_end_time + 1 + chartinfo.max_end_time // 5, 5))
        gnt.set_xticks(np.arange(0, chartinfo.max_end_time + 1 + chartinfo.max_end_time // 5), minor=True)

        gnt.grid(which='major', axis='x', color='blue', alpha=0.8, dashes=(3, 3))
        gnt.grid(which='minor', axis='x', color='gray', alpha=0.5, dashes=(3, 3))

        # Draw
        list_already_draw = []
        for i in range(len(list_charts)):
            for scheinfo in list_charts[i]:
                if scheinfo.get_process() in list_already_draw:
                    gnt.broken_barh([(scheinfo.get_start_time(), scheinfo.get_last_time())], ((i * 10 + 7, 6)),
                                    facecolors=(scheinfo.get_color()))
                else:
                    list_already_draw.append(scheinfo.get_process())
                    gnt.broken_barh([(scheinfo.get_start_time(), scheinfo.get_last_time())], ((i * 10 + 7, 6)),
                                    facecolors=(scheinfo.get_color()), label=str(scheinfo.get_process().get_id()))
        if val_return != []: gnt.legend(loc="best")
        self.canvas.draw()


    def state_radioBtn(self):
        self.init_push()
        if self.btn_PSPN.isChecked():
            self.input_priority_enabled = True
            self.input_priority.setEnabled(True)

            for i in range(len(self.psList)):
                self.table_process.setItem(i, 3, QTableWidgetItem(str(self.psList[i].get_priority())))

            sname = "PSPN"
        else :
            self.input_priority_enabled = False
            self.input_priority.setEnabled(False)

            for i in range(len(self.psList)):
                self.table_process.setItem(i, 3, QTableWidgetItem('1'))

            sname = "other"

        print("state: ", sname)


    def init_push(self):
        self.input_at.setText("")
        self.input_bt.setText("")
        self.input_priority.setText("1")
        id = 1
        while ("P" + str(id)) in self.idList: id += 1
        self.input_id.setText("P" + str(id))

    # 프로세스 입력 state
    def state_push(self):
        process_id = self.input_id.text()
        process_at = self.input_at.text()
        process_bt = self.input_bt.text()
        process_priority = self.input_priority.text()

        # 3가지 경우
        # 빈칸이 존재
        # 잘못된 값 (not digit or at, bt <= 0)
        # 프로세스가 이미 15개
        error = True
        msg = ''
        if process_id == "" or process_at == "" or process_bt == "":
            msg = ''
        elif self.input_priority_enabled and process_priority == "":
            msg = ''
        elif len(self.psList) >= 15:
            msg = "최대 프로세스는 15개 입니다."
        elif process_id in self.idList:
            msg = '이미 존재하는 ID입니다.'
        elif (not process_at.isdigit() or int(process_at) < 0) and (not process_bt.isdigit() or int(process_bt) <= 0):
            msg = 'Wrong Input'
        elif not process_at.isdigit() or int(process_at) < 0:
            msg = 'Wrong Input : AT'
        elif not process_bt.isdigit() or int(process_bt) <= 0:
            msg = 'Wrong Input : BT'
        elif self.input_priority_enabled and (not process_priority.isdigit() or int(process_priority) < 0):
            msg = 'Wrong Input : Priority'
        elif int(process_at) > 100 or int(process_bt) > 100 or (self.input_priority_enabled and int(process_priority) > 100):
            msg = '최대값은 100입니다.'
        else : error = False

        if error :
            self.label_state_process.setText(msg)
            self.btn_push.setEnabled(False)
            self.btn_push_enabled = False
        else :
            self.label_state_process.setText("")
            self.btn_push.setEnabled(True)
            self.btn_push_enabled = True


    # 프로세스 입력 버튼
    def command_push(self):
        if not self.btn_push_enabled : return
        if len(self.psList) >= 15 : return

        process_id = self.input_id.text()
        process_at = self.input_at.text()
        process_bt = self.input_bt.text()
        if self.input_priority_enabled: process_priority = self.input_priority.text()
        else : process_priority = '1'


        #print("qppend!")
        self.psList.append(Process(process_id, int(process_at), int(process_bt), int(process_priority)))
        self.idList.add(process_id)

        self.table_process.setItem(self.count, 0, QTableWidgetItem(str(process_id)))
        self.table_process.setItem(self.count, 1, QTableWidgetItem(str(int(process_at))))
        self.table_process.setItem(self.count, 2, QTableWidgetItem(str(int(process_bt))))
        self.table_process.setItem(self.count, 3, QTableWidgetItem(str(int(process_priority))))

        self.table_process.scrollToItem(self.table_process.item(self.count, 0))

        self.count += 1
        self.init_push()

        if not self.btn_start_enabled:
            self.btn_start_enabled = True
            self.btn_start.setEnabled(True)

        if not self.btn_reset_enabled:
            self.btn_reset_enabled = True
            self.btn_reset.setEnabled(True)

    # 프로세스 reset 버튼
    def command_reset(self):
        if not self.btn_reset_enabled: return
        if self.count <= 0: return

        self.idList.clear()
        self.psList.clear()

        self.count = 0
        self.init_push()
        self.init_timeQuantum()

        self.set_table()

        self.btn_start_enabled = False
        self.btn_start.setEnabled(False)

        self.btn_reset_enabled = False
        self.btn_reset.setEnabled(False)

        self.table_process.scrollToItem(self.table_process.item(0, 0))

        chartinfo.reset()

        self.set_chart()

    def command_delete(self, row, column):
        if row >= self.count : return

        self.idList.remove(self.psList[row].get_id())
        self.psList.pop(row)

        self.count -= 1
        self.init_push()

        self.set_table()

        if self.count <= 0:
            self.btn_start_enabled = False
            self.btn_start.setEnabled(False)

            self.btn_reset_enabled = False
            self.btn_reset.setEnabled(False)
        else :
            self.table_process.scrollToItem(self.table_process.item(self.count-1, 0))

    def init_timeQuantum(self):
        self.input_timeQuantum.setText(str(self.request.get_timeQuantum()))

    # time_quantum state
    def state_timeQuantum(self):
        tq = self.input_timeQuantum.text()
        if tq == '':
            self.label_state_timeQuantum.setText("")
        elif not tq.isdigit() or int(tq) <= 0:
            self.label_state_timeQuantum.setText("Wrong Input")
        else :
            self.label_state_timeQuantum.setText("")
            self.request.set_timeQuantum(int(tq))

            #print("timeQuantum :", self.request.get_timeQuantum())
    # 실행버튼
    def command_start(self):
        num_of_processor = 1
        if self.btn_cn1.isChecked(): num_of_processor = 1
        elif self.btn_cn2.isChecked(): num_of_processor = 2
        elif self.btn_cn3.isChecked(): num_of_processor = 3
        elif self.btn_cn4.isChecked(): num_of_processor = 4
        self.request.set_coreNumber(num_of_processor)

        time_quantum = self.request.get_timeQuantum()
        print("time_quantum:", time_quantum)
        print("num_of_processors: ", num_of_processor)

        # input label 정리
        self.init_timeQuantum()
        self.init_push()

        for ps in self.psList:
            ps.reset()
        chartinfo.reset()

        # 스케줄링 작업
        if self.btn_FCFS.isChecked():
            scheduler = FCFS(self.psList, self.request)
            sname = "FCFS"
        elif self.btn_RR.isChecked():
            scheduler = RR(self.psList, self.request)
            sname = "RR"
        elif self.btn_SPN.isChecked():
            scheduler = SPN(self.psList, self.request)
            sname = "SPN"
        elif self.btn_SRTN.isChecked():
            scheduler = SRTN(self.psList, self.request)
            sname = "SRTN"
        elif self.btn_PSPN.isChecked():
            scheduler = PSPN(self.psList, self.request)
            sname = "PSPN"
        else :
            scheduler = HRRN(self.psList, self.request)
            sname = "HRRN"

        print(sname)

        try:
            val_return = scheduler.scheduling()
        except:
            msg = QMessageBox()
            msg.setText("Scheduler Error: " + sname)
            msg.exec_()
        else:
            # 차트 그리기
            self.set_chart(val_return)

            # 테이블 수정
            self.set_table()

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
