# 이름 : 엄희용
# 학번 : 2019136080
# 2021. 4. 10.

from chartinfo import chartinfo

class Processor:
    def __init__(self):
        # process = 현재 프로세서에서 작업중인 프로세스
        self.__process = None
        # rbt = 실행 후 남아있는 bt
        self.__rbt = 0
        self.__start_time = -1
        self.__list_chart = []

    def set_process(self, process, time):
        self.__process = process
        self.__rbt = process.get_bt()
        self.__start_time = time

    # 작업이 끝나면 프로세스를 반환
    def work(self, time):
        if(self.__rbt > 0):
            self.__rbt -= 1
        
        if(self.__rbt == 0):
            self.__note(time)
            pro = self.__process
            self.__resetting()
            return pro
        
        return None

    # 프로세서스는 몇 초부터 몇 초까지 어떤 프로세스를 일했는지 기록
    def __note(self, time):
        last_time = time + 1 - self.__start_time
        self.__list_chart.append(chartinfo(self.__start_time, time+1, last_time, self.__process))

    def get_log(self):
        return self.__list_chart

    # 프로세서 멤버변수 초기화
    def __resetting(self):
        self.__process = None
        self.__start_time = -1
        self.__rbt = 0

    # 프로세서에 프로세스가 할당되었는지
    def isempty(self):
        return True if self.__process == None else False
    
    def isworking(self):
        return False if self.__process == None else True