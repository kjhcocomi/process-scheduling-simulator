from scheduleInfo import Process

class chartinfo:
    # start_time: 프로세서가 일하기 시작한 시각
    # end_time: 프로세서가 해당 프로세스의 일을 끝낸 시각
    # last_time: 몇초동안 일을 했는지
    # process: 어떤 프로세스인지 - scheduleinfo.py에 있는 Process 객체를 넣어주세요

    # ex) 1초에 시작 3초에 종료
    # start_time = 1
    # end_time = 3
    # last_time = 2

    # 객체를 생성할 때 end_time이나 last_time을 모른다면 일단 0으로 만들고
    # set end_time이나 set last_time으로 둘중 하나를 설정한다면 나머지 하나는 자동으로 설정되게 만들었습니다.
    # 밑에 한번 확인해 주세요
    list_color = ["black", "orange", "green", "navy", "gray", "yellow", "aqua", "purple", "coral", "olive", "deepskyblue", "crimson", "chocolate", "teal", "hotpink"]
    dict_process = {}
    num_of_process = 0
    max_end_time = 0
    def __init__(self, start_time, end_time, last_time, process):
        self.__start_time = start_time
        self.__end_time = end_time
        self.__last_time = last_time
        self.__process = process
        chartinfo.max_end_time = max(chartinfo.max_end_time, end_time)
        if process in chartinfo.dict_process:
            self.__color = chartinfo.dict_process[process]
        else:
            self.__set_color()
    def print(self):
        print(self.__start_time, self.__end_time, self.__last_time)
    def get_start_time(self):
        return self.__start_time
    def set_start_time(self, start_time):
        self.__start_time = start_time

    def get_end_time(self):
        return self.__end_time
    def set_end_time(self, end_time):
        self.__end_time = end_time
        self.__last_time = end_time - self.__start_time
        chartinfo.max_end_time = max(chartinfo.max_end_time, end_time)
    
    def get_last_time(self):
        return self.__last_time
    def set_last_time(self, last_time):
        self.__last_time = last_time
        self.__end_time = self.__start_time + last_time
        chartinfo.max_end_time = max(chartinfo.max_end_time, self.__end_time)

    def get_process(self):
        return self.__process
    def set_process(self, process):
        self.__process = process

    def __set_color(self):
        chartinfo.dict_process[self.__process] = chartinfo.list_color[chartinfo.num_of_process]
        self.__color = chartinfo.list_color[self.num_of_process]
        chartinfo.num_of_process += 1

    def get_color(self):
        return self.__color

    @classmethod
    def reset(cls):
        cls.dict_process = {}
        cls.num_of_process = 0
        cls.max_end_time = 0