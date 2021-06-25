# 이름 : 김지우
# 학번 : 2017136024
# 2021. 4. 9.

from scheduleInfo import Process
from scheduleInfo import Request
from chartinfo import chartinfo
from collections import deque

class RR:
    # process_list : process 클래스 리스트
    # request : core_number, time_quantum 정보가 담겨있음
    def __init__(self, processList, request):
        self.__process_list = processList
        self.__request = request

    #
    def scheduling(self):
        psList=self.__process_list
        coreNum=self.__request.get_coreNumber()
        readyQueue = deque()#각프로세스 번호저장
        core=[False for i in range(coreNum)]#각 코어가 동작하는지
        timeQuantum=[self.__request.get_timeQuantum() for i in range(coreNum)]#각 코어의 단위시간 흐름
        remainingTime=[]#각 프로세스별 남은 시간
        for i in range(0,len(psList)):
            if i==0:
                remainingTime.append(psList[i].get_bt())
            else:
                remainingTime.append(psList[i].get_bt())#각 프로세스별 남은 시간저장
        nowProcess=[-1]*coreNum
        ganttList=[deque() for i in range(coreNum)]#간트차트
        nowTime=0#현재 시간
        endedNumber=0
        while True:
            
            for i in range (0,len(psList)):#첫번째 프로세스를 제외한 나머지 프로세스를 시간대에 맞게 넣는다
                    if psList[i].get_at()==nowTime and (remainingTime[i]>0)==True:
                        readyQueue.append(i)
            for i in range(0,coreNum):#0초일때동작안함
                if core[i]==True:
                    timeQuantum[i]-=1
                    remainingTime[nowProcess[i]]-=1
                    if timeQuantum[i]>0:#단위시간이 안끝난경우
                        if remainingTime[nowProcess[i]]<=0:#현재 프로세스의 실행시간이 끝난 경우
                            print(nowProcess[i])
                            psList[nowProcess[i]].set_tt(nowTime-psList[nowProcess[i]].get_at())
                            endedNumber+=1#끝난 프로세스개수
                            nowProcess[i]=-1#현재 프로세스 없애기
                            core[i]=False#코어 작동안함
                            timeQuantum[i]=self.__request.get_timeQuantum()#타임퀀텀 초기화   
                    elif timeQuantum[i]<=0:#단위시간이 끝난경우
                        if remainingTime[nowProcess[i]]==0 :#현재 프로세스의 실행시간이 끝난경우
                            print(nowProcess[i])
                            psList[nowProcess[i]].set_tt(nowTime-psList[nowProcess[i]].get_at())
                            endedNumber+=1#끝난 프로세스개수
                            nowProcess[i]=-1#현재 프로세스 없애기
                            core[i]=False#코어 작동안함
                            timeQuantum[i]=self.__request.get_timeQuantum()#타임퀀텀 초기화
                        elif remainingTime[nowProcess[i]]>0:#현재 프로세스의 실행시간이 남은 경우
                            readyQueue.append(nowProcess[i])#레디큐에 추가
                            core[i]=False#코어 작동안함
                            nowProcess[i]=-1
                            timeQuantum[i]=self.__request.get_timeQuantum()#타임퀀텀 초기화
            
            for i in range(0,coreNum):
                if core[i]==False:
                    if readyQueue:
                        nowProcess[i]=readyQueue.popleft()
                        timeQuantum[i]=self.__request.get_timeQuantum()
                        core[i]=True
            for i in range(0,coreNum):
                ganttList[i].append(nowProcess[i])
            
            if endedNumber==len(psList):
                break
            nowTime+=1
            
        for i in psList:#WT,NTT계산
            i.set_wt(i.get_tt()-i.get_bt())
            i.set_ntt(i.get_tt()/i.get_bt())
        chartInfoList=[]
        for i in range(0, len(ganttList)):
            nowGantt = ganttList[i][0]
            ganttTime = 0
            testList = []
            for j in range(0, len(ganttList[i])):

                if nowGantt != ganttList[i][j] :
                    if ganttList[i][ganttTime]!=-1:
                        x=chartinfo(ganttTime,j,self.__request.get_timeQuantum()+((j-ganttTime)-self.__request.get_timeQuantum()),psList[ganttList[i][ganttTime]])
                        testList.append(x)
                    nowGantt = ganttList[i][j]
                    ganttTime = j
                if j+1==len(ganttList[i]):
                    if ganttList[i][ganttTime]!=-1:
                        x=chartinfo(ganttTime,j+1,self.__request.get_timeQuantum()+((j+1-ganttTime)-self.__request.get_timeQuantum()),psList[ganttList[i][ganttTime]])
                        testList.append(x)


            chartInfoList.append(testList)

        return chartInfoList # 스케줄링 완료된 readyQueue 반환

if __name__ == "__main__" :

    psList = []
    psList.append(Process(1,0, 3))
    psList.append(Process(2,1, 7))
    psList.append(Process(3,3, 2))
    psList.append(Process(4,5, 5))
    psList.append(Process(5,6, 3))
    request = Request()
    request.set_coreNumber(1)
    request.set_timeQuantum(3)
    scheduler = RR(psList, request)
    q = scheduler.scheduling()
    for i in psList:
        print(i.get_wt()," ",i.get_tt()," ",i.get_ntt())