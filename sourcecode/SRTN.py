# 이름 : 박동주
# 학번 : 2017136042
# 2021. 4. 7.


from scheduleInfo import Process
from scheduleInfo import Request
from chartinfo import chartinfo
from collections import deque

from time import sleep

class SRTN:
    # process_list : process 클래스 리스트
    # request : core_number, time_quantum 정보가 담겨있음
    def __init__(self, processList, request):
        self.__processList = processList
        self.__request = request

    def scheduling(self):
        core_num = self.__request.get_coreNumber()
        ps_list = self.__processList

        retList = [deque() for i in range(core_num)]

        Time = 0

        # 잔여 실행시간
        #bt = [0] * 15
        bt = dict()
        for ps in ps_list: bt[ps.get_id()] = ps.get_bt()

        idToProcess = dict()
        for ps in ps_list: idToProcess[ps.get_id()] = ps

        # 실행중인 프로세스 id
        runningProcessId = set()

        while sum(bt.values()) > 0:
            # 대기중인 프로세스 id
            waitingProcessId = []
            for i in range(len(ps_list)):
                id = ps_list[i].get_id()
                if bt[id] > 0 and ps_list[i].get_at() <= Time and id not in runningProcessId:
                    waitingProcessId.append(id)

            # 대기중인 프로세스가 있으면?
            # 1. 비어있는 코어에 추가
            # 2. 실행시간을 비교 후 자리를 뺐음
            if len(waitingProcessId) > 0:
                # 잔여 실행시간 기준으로 정렬
                waitingProcessId.sort(key=lambda x: bt[x])

                # 적재 완료된 코어
                load_complete = [False] * core_num

                # 비어있는 코어에 프로세스 추가
                for i in range(core_num):
                    if len(waitingProcessId) == 0: break
                    if len(retList[i]) == 0 or retList[i][-1].get_process().get_id() not in runningProcessId:
                        id = waitingProcessId.pop(0)
                        #newProcess = Process(id, Time, 0)
                        newProcess = chartinfo(Time, 0, 0, idToProcess[id])
                        retList[i].append(newProcess)
                        load_complete[i] = True
                        runningProcessId.add(id)

                # 프로세스 뺐어야 하는 경우 탐색
                for i in range(core_num):
                    if len(waitingProcessId) == 0: break
                    if load_complete[i] : continue

                    # 뺐어야 하는 경우 : 실행중인 프로세스보다 잔여 실행시간이 작은 게 있으면
                    ps = retList[i][-1].get_process()
                    currBt = bt[ps.get_id()]
                    if currBt > bt[waitingProcessId[0]]:
                        runningProcessId.remove(ps.get_id())
                        id = waitingProcessId.pop(0)
                        #newProcess = Process(id, Time, 0)
                        newProcess = chartinfo(Time, Time, 0, idToProcess[id])
                        retList[i].append(newProcess)
                        runningProcessId.add(id)

            # 실행중인 프로세스 실행시간 +1
            # 실행중인 프로세스 잔여 실행시간 -1
            # 실행시간 0인 id를 runningProcessId에서 제거
            for i in range(core_num):
                if len(retList[i]) == 0: continue

                chartinfo1 = retList[i][-1]
                ps = chartinfo1.get_process()
                if ps.get_id() in runningProcessId:
                    chartinfo1.set_end_time(Time + 1)

                    id = ps.get_id()
                    bt[id] -= 1
                    if bt[id] <= 0:
                        runningProcessId.remove(id)
                        tt = Time + 1 - idToProcess[id].get_at()
                        wt = tt - idToProcess[id].get_bt()
                        ntt = tt / idToProcess[id].get_bt()

                        idToProcess[id].set_tt(tt)
                        idToProcess[id].set_wt(wt)
                        idToProcess[id].set_ntt(ntt)

            Time += 1

        return retList # 스케줄링 완료된 retList 반환



if __name__ == "__main__" :
    psList = []
    psList.append(Process(0, 0, 3))
    psList.append(Process(1, 1, 7))
    psList.append(Process(2, 3, 2))
    psList.append(Process(3, 5, 5))
    psList.append(Process(4, 6, 3))

    request = Request()
    request.set_coreNumber(4)
    request.set_timeQuantum(2)

    scheduler = SRTN(psList, request)
    q = scheduler.scheduling()
    '''
    for i in range(len(q)):
        for j in range(len(q[i])):
            print('PID%d %ds' % (q[i][j].get_id(), q[i][j].get_bt()), end=' | ')
        print()
    '''