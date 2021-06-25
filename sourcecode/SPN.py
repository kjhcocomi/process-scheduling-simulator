# 이름 : 엄희용
# 학번 : 2019136080
# 2021. 4. 07.

from scheduleInfo import Process
from scheduleInfo import Request
from chartinfo import chartinfo
from Processor import Processor

class SPN:
    # process_list : process 클래스 리스트
    # request : core_number, time_quantum 정보가 담겨있음
    def __init__(self, processList, request):
        self.__processList = processList
        self.__request = request

    def scheduling(self):
        core_num = self.__request.get_coreNumber()
        ps_list = self.__processList.copy()
        pr_list = [Processor() for i in range(core_num)]

        readyQueue = []

        i = 0 # 현재시간
        while True:

            isdone = True
            for pr in pr_list:
                if pr.isworking():
                    isdone = False
                    break
            
            # 종료 조건
            if isdone and len(readyQueue) == 0 and len(ps_list) == 0: break

            # 프로세스의 도착시간과 현재시간이 일치하면 레디큐에 프로세스 추가
            for ps in ps_list[:]:
                if ps.get_at() == i:
                    readyQueue.append(ps)
                    ps_list.remove(ps)
            
            # BT가 작은 숫자부터 오름차순 정렬
            readyQueue.sort(key=lambda ps: ps.get_bt())
            
            # 프로세스를 레디큐에서 프로세서에 할당
            for ps in readyQueue[:]:
                for pr in pr_list:
                    if pr.isempty():
                        pr.set_process(ps, i)
                        readyQueue.remove(ps)
                        break

            # 프로세서 작업
            for pr in pr_list:
                if pr.isworking():
                    endprocess = pr.work(i)

                    # 작업이 끝난 프로세스 정보 저장
                    if endprocess != None:
                        endtime = i + 1
                        endprocess.set_tt(endtime - endprocess.get_at())
                        endprocess.set_wt(endprocess.get_tt() - endprocess.get_bt())
                        endprocess.set_ntt(endprocess.get_tt() / endprocess.get_bt())

            
            # 시간 증가
            i += 1
        
        # GUI에서 Chart를 그리기 위한 Processor Log 반환
        list_return = []

        for i in pr_list:
            list_return.append(i.get_log())
        return list_return

# TEST
# psList = []
# psList.append(Process(0, 0, 3))
# psList.append(Process(1, 1, 7))
# psList.append(Process(2, 3, 2))
# psList.append(Process(3, 5, 5))
# psList.append(Process(4, 6, 3))

# request = Request()
# request.set_coreNumber(1)
# request.set_timeQuantum(2)

# scheduler = SPN(psList, request)
# scheduler.scheduling()

# for i in psList:
#     print("Process ID: {0}, AT: {1}, BT: {2}, WT: {3}, TT: {4}, NTT: {5}".format(i.get_id(), i.get_at(), i.get_bt(), i.get_wt(), i.get_tt(), i.get_ntt()))