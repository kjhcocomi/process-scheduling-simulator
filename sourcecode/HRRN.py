# 이름 : 김종현
# 학번 : 2017136023
# 2021. 4. 09.


from scheduleInfo import Process
from scheduleInfo import Request
from collections import deque
from chartinfo import chartinfo

class HRRN:
    # process_list : process 클래스 리스트
    # request : core_number, time_quantum 정보가 담겨있음
    def __init__(self, processList, request):
        self.__processList = processList
        self.__request = request


    def scheduling(self):
        core_num = self.__request.get_coreNumber()
        ps_list = self.__processList

        processQueue = [deque() for i in range(core_num)]

        response_ratio=[]  # HRRN 방식에서 필요한 response_ratio 생성
        wt=[] # 프로세스의 현재 waiting time
        bt=[] # 프로세스의 현재 burst time
        for i in range(0,len(ps_list)):
            response_ratio.append(0)
            wt.append(0)
            bt.append(0)

        returnlist=[]
        
        ongoing=[] #프로세서가 일을 진행중인지의 여부
        for i in range(0,core_num):
            ongoing.append(False)  

        time=0 #시간
        finishcount=0 #while문 종료조건
        while 1:
            for i in range(0,len(ps_list)):  # 모든 프로세스들을 비교
                if ps_list[i].get_at()==time:  #현재 시간과 arrival time이 같으면 arrive time을 true로
                    ps_list[i].set_arrived()  # 프로세스 도착
                if (ps_list[i].get_arrived()==True) & (ps_list[i].get_progress()==False): # 현재 도착한 상태이고 일을 진행중이지 않을 때
                    wt[i]=time-ps_list[i].get_at() # waiting time= 현재시간-arrival time
                    response_ratio[i]=(ps_list[i].get_bt()+wt[i])/ps_list[i].get_bt() # response ratio 계산
            

            for c in range(0,core_num):
                if ongoing[c]==False:  #프로세서가 일을 하지 않고 있다면
                    ratiolist=[]  # response ration값들을 저장하기 위한 리스트
                    for i in range(0,len(ps_list)): 
                        if (ps_list[i].get_arrived()==True) & (ps_list[i].get_progress()==False): # 프로세서에 도착하고 일을 진행중이지 않은 프로세스들 중에서
                            ratiolist.append([response_ratio[i],i,ps_list[i].get_bt()])   # response ratio 값과 프로세스 번호를 리스트에 삽입
                    if len(ratiolist)>0: # 리스트에 값이 있으면
                        maxindex=0
                        max=0
                        for j in range(0,len(ratiolist)):
                            if ratiolist[j][0]>max:
                                max=ratiolist[j][0]
                                maxindex=ratiolist[j][1]
                        if max==1:
                            minbt=ratiolist[0][2]
                            for j in range(0,len(ratiolist)):
                                if ratiolist[j][2]<minbt:
                                    minbt=ratiolist[j][2]
                                    maxindex=ratiolist[j][1]
                        ps_list[maxindex].set_progress() # progress를 true로 바꿔 해당 프로세스가 일을 하는 중 이라고 바꾼다
                        ps_list[maxindex].set_where(c)   # 프로세스가 어느 프로세서에서 일하는지
                        ongoing[c]=True # 프로세서가 일을 하는 중으로 바꾼다
                    

            for c in range(0,core_num):
                if ongoing[c]==True:
                    for i in range(0,len(ps_list)):
                        if (ps_list[i].get_progress()==True) & (ps_list[i].get_finished()==False) & (ps_list[i].get_where()==c):                           
                            if bt[i]+1==ps_list[i].get_bt(): # 프로세스의 현재 수행 시간과 프로세스의 수행 시간이 같으면 일을 그만함.
                                ongoing[c]=False #프로세스가 일을 끝냈으니 프로세서는 현재 쉬는상태
                                finishcount+=1     # 하나의 프로세스가 일을 마치면 finishcount 증가
                                ps_list[i].set_finished() #해당 프로세스의 일이 끝났다고 표시
                                processQueue[c].append(ps_list[i]) #프로세스 큐에 삽입


            if finishcount==len(ps_list):    # finishcount가 프로세스 수와 같아지면 while문 탈출
                break

            # 일을 진행중이고 끝나지 않은 프로세스의 현재 수행시간 증가
            for i in range(0,len(ps_list)):
                if (ps_list[i].get_progress()==True) & (ps_list[i].get_finished()==False):
                    bt[i]+=1
            time+=1

        # wt, tt, ntt 설정    
        for i in range(0,len(ps_list)):
            ps_list[i].set_wt(wt[i])
            ps_list[i].set_tt(ps_list[i].get_bt()+wt[i])
            ps_list[i].set_ntt(ps_list[i].get_tt()/ps_list[i].get_bt())
            print(str(i+1)+" Process: "+str(ps_list[i].get_id())+"     "+str(ps_list[i].get_at())+"     "+str(ps_list[i].get_bt())+"     "+str(ps_list[i].get_wt())+"     "+str(ps_list[i].get_tt())+"     "+str(ps_list[i].get_ntt()))
        
        
        # chartinfo 형식에 맞게 변환
        for i in range(0,core_num):
            returnlist.append([])
            for j in range(0,len(processQueue[i])):
                returnlist[i].append(chartinfo(processQueue[i][j].get_at()+processQueue[i][j].get_wt(),processQueue[i][j].get_at()+processQueue[i][j].get_wt()+processQueue[i][j].get_bt(),processQueue[i][j].get_bt(),processQueue[i][j]))
        
        #return processQueue
        return returnlist # returnlist 반환



if __name__ == "__main__" :
    psList = []
    n_o_processes=eval(input("number of processes: "))
    n_o_processors=eval(input("number of processors: "))
    for i in range(0,n_o_processes):
        at=eval(input(str(i+1)+'번째 arrival time: '))
        bt=eval(input(str(i+1)+"번째 burst time: "))
        psList.append(Process(i+1,at,bt))



    request = Request(0,n_o_processors)

    scheduler = HRRN(psList, request)


    q = scheduler.scheduling()

    #print(q[0][4].get_end_time())

    #for i in range(len(q)):
    #    for j in range(len(q[i])):
    #        print('PID%d %ds' % (q[i][j].get_id(), q[i][j].get_bt()), end=' | ')
    #    print()