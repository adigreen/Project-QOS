

import random
import math
import matplotlib.pyplot as plt



def Simulation(T,r,B,printInFuncDebug):
    #Building random first state
    randHelp=random.random()
    if randHelp>=0.5:
        state = 1                 #1=ON 0=OFF
    else:
        state = 0

    
    #choose lamda (lambda is taken in python :(   )
    lamda = 5
    miu=10
    teta=10
    k=8
    #Probabilities
    p10 = (r)/(B)      #probability to change state from state ON to OFF
    p01 = (B-r)/(B)    #probability to change state from state OFF to ON
    
    #Code parameters
    numberOfPackets = 0
    interPacketCount = 0
    timeSum = 0
    packetsTimesList = []
    avgBurst=[]
    queue=[]
    lastqueue = 0
    d = 3
    busy = 0
    power_vection = []
    power_novectio = []
    alive_servers = k
    power=10
    interval=0
    busy=0
    interval2=0
    servers2=0
    
    if(printInFuncDebug): 
        print('p10='+str(p10)+' p01='+str(p01))
    
    i = 0

    for l in range(T+1):
        power_vection.insert(l, 0)
        power_novectio.insert(l, 0)


    while(timeSum<T):
        outerTimeUnitCounter = 0
        interPacketCount = 0
        ##ON state
        if(state): 
            '''
            Making the transition between states of the markov chain
            '''
            randHelp=random.random()
            if randHelp>=p10:
                state = 0
            else:
                state = 1

            interTimeUnitCounter = 0


            ##generate packet
            time_help=timeSum
            while interTimeUnitCounter<1 and timeSum<i+1: #while still in the time unit create all of the burst    
                numberOfPackets+=1
                '''
                If we want to make a Poisson process, times between arrivals are 
                exponentially distributed. Exponential values can be generated with the 
                inverse CDF method: -k*log(u) where u is a uniform random variable and
                k is the mean of the exponential (k=1/ λ)--> log(u)/ λ
                '''
                interTimeUnit = -math.log(1-random.uniform(0,1))/(lamda)
                interTimeUnitCounter = interTimeUnitCounter + interTimeUnit
                timeSum = timeSum + interTimeUnit
                packetsTimesList.append(timeSum)
                interPacketCount += 1
                if(printInFuncDebug):     
                    print(str(interPacketCount) +' ,inter-TU:' + str(interTimeUnit) + ' , timestamp:' + str(timeSum))
            if(printInFuncDebug): 
                print(str(interPacketCount)+" packets sent")
            avgBurst.append(interPacketCount)
            i += 1
            if(i<T):
                if(printInFuncDebug): 
                    print("#############Interval between:"+str(i+1)+'-'+str(i)+"[timeUnit]##############")
        #OFF state     
        else: 
            '''
            Making the transition between states of the markov chain
            '''
            #if state is OFF change state with probability p01
            randHelp=random.random()
            if randHelp>=p01:
                state = 1
            else:
                state = 0
            if(printInFuncDebug): 
                print("no packet")
            time_help = timeSum
            timeSum += 1
            
            
            i += 1 
            if(i<T):
                if(printInFuncDebug): 
                    print("#############Interval between:"+str(i+1)+'-'+str(i)+"[timeUnit]##############")


        adding_to_queue = lastqueue + interPacketCount -1
        if adding_to_queue<0:
            adding_to_queue=0


        while outerTimeUnitCounter < 1 and time_help < i :
            # check when the vecation time is over if we have servers at vecation
            if(time_help>interval2):
                busy=busy-servers2
                if busy<0:
                    busy=0
            if (time_help>interval):
                if(adding_to_queue>(k-d)):
                    alive_servers=k
                else:
                    interval = time_help + -math.log(1 - random.uniform(0, 1)) / (teta)

            #processes leaving the queue+check if there are free servers
            exitTimeUnit = -math.log(1 - random.uniform(0, 1)) / (miu)
            outerTimeUnitCounter = outerTimeUnitCounter + exitTimeUnit
            timeSumouter = time_help + exitTimeUnit

            if(adding_to_queue>0):
                interval2=time_help+1
                if(adding_to_queue>(alive_servers-busy)):
                    adding_to_queue=adding_to_queue-(alive_servers-busy)
                    servers2=busy
                    busy=alive_servers
                else:
                    servers2=busy
                    busy = busy +adding_to_queue
                    adding_to_queue=0
            # checking if need to turn off servers in the last time unit
            else:
                if(alive_servers==k):
                    alive_servers=k-d
                    if(alive_servers<busy):
                        alive_servers=k
                interval = time_help + -math.log(1 - random.uniform(0, 1)) / (teta)



        queue.append(adding_to_queue)
        lastqueue=adding_to_queue


        power_vection[i]=power*busy+0.5*power*(alive_servers-busy)+0.25*(k-alive_servers)
        power_novectio[i]=power*busy+0.5*power*(k-busy)

    return power_vection,power_novectio



if __name__=='__main__':
    avarge_vecation=[]
    avarge_Novecation=[]

    for l in range(11):
        avarge_vecation.insert(l, 0)
        avarge_Novecation.insert(l, 0)

    for i in range(100):
        S1,S2=Simulation(T=10,r=5,B=10,printInFuncDebug=False)
        for k in range(11):
            avarge_vecation[k]+=S1[k]
            avarge_Novecation[k]+=S2[k]

    sum_vec=0
    sum_nvec=0
    for i in range(11):
        avarge_vecation[i]=avarge_vecation[i]/100
        avarge_Novecation[i]=avarge_Novecation[i]/100
        sum_vec+=avarge_vecation[i]
        sum_nvec+=avarge_Novecation[i]


    print("E vecation: "+str(sum_vec/11))
    print("E with out vecation: "+str(sum_nvec/11))



    fig = plt.figure()
    fig.suptitle('Energy Consumption')

    plot, = plt.plot(range(len(S1)), S1,color = 'red', marker = '.', linestyle = '-',label='M/M/k with vacation')
    plot, = plt.plot(range(len(S2)), S2, color = 'blue', marker = '.', linestyle = '-',label='Regular M/M/K')
    plt.legend()
    plt.xlabel('Time Unit')
    plt.ylabel('energy consumption')

    plt.show()



