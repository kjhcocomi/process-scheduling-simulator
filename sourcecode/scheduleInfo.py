class Process:
    def __init__(self, id, at=0, bt=0, priority=1):
        self.__id = id
        self.__at = at
        self.__bt = bt
        self.__wt = 0
        self.__tt = 0
        self.__ntt = 0

        # 프로세스의 우선순위
        self.__priority = priority

        # 프로세서가 어느 코어에서 일하고있는지
        self.__where = 0

        # 도착여부, 일이 끝났는지에 대한 여부, 일 진행중인지에 대한 여부를 추가하였다.
        self.__arrived = False
        self.__finished = False
        self.__progress = False

    def get_id(self):
        return self.__id

    def get_at(self):
        return self.__at

    def get_bt(self):
        return self.__bt

    def set_bt(self, bt):
        if bt >= 0: self.__bt = bt

    def get_wt(self):
        return self.__wt

    def set_wt(self, wt):
        if wt >= 0: self.__wt = wt

    def get_tt(self):
        return self.__tt

    def set_tt(self, tt):
        if tt >= 0: self.__tt = tt

    def get_ntt(self):
        return self.__ntt

    def set_ntt(self, ntt):
        if ntt >= 0: self.__ntt = ntt

    def get_priority(self):
        return self.__priority

    def reset(self):
        self.__wt = 0
        self.__tt = 0
        self.__ntt = 0
        self.__where = 0
        self.__arrived = False
        self.__finished = False
        self.__progress = False

    # 추가한 메소드들
    def get_where(self):
        return self.__where

    def set_where(self, where):
        if where >= 0 & where <= 4: self.__where = where

    def get_arrived(self):
        return self.__arrived

    def set_arrived(self):
        self.__arrived = True

    def get_finished(self):
        return self.__finished

    def set_finished(self):
        self.__finished = True

    def get_progress(self):
        return self.__progress

    def set_progress(self):
        self.__progress = True


class Request:
    def __init__(self, t=0, c=1):
        self.__time_quantum = t
        self.__core_number = c

    def get_timeQuantum(self):
        return self.__time_quantum

    def set_timeQuantum(self, t):
        if t >= 0: self.__time_quantum = t

    def get_coreNumber(self):
        return self.__core_number

    def set_coreNumber(self, c):
        if c >= 1 and c <= 4:
            self.__core_number = c
