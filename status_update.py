# -*-coding: utf-8 -*-

import csv
import json

#===================================================#

#data input of present data
with open('tempD.csv', 'rb') as csvfile:
    spamreader  = csv.reader(csvfile,delimiter=',')
    totalD = list(spamreader)

nowdata = totalD[len(totalD)-1]

#===================================================#

#data input of logged data
with open('monitoring_status.json') as statusfile:
    data = json.load(statusfile)

recorddata = [data["current"]["time"], data["current"]["temperature"], data["current"]["humidity"]]

#===================================================#

#variable definition of nowdata (for inspection values into region)
def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


nowtime = nowdata[0]
nowtemp = num(nowdata[1])
nowhum = num(nowdata[2])

#===================================================#
#data inspection (nowdata)

# : duplicate hystereses and configuring regions

lowest = 0
highest = 100

inspect_temp = [lowest,num(data["hysteresis"]["low"]["send"]["temperature"]), num(data["hysteresis"]["low"]["reset"]["temperature"]), num(data["hysteresis"]["high"]["reset"]["temperature"]), num(data["hysteresis"]["low"]["send"]["temperature"]) ,highest]
inspect_hum = [lowest,num(data["hysteresis"]["low"]["send"]["humidity"]), num(data["hysteresis"]["low"]["reset"]["humidity"]), num(data["hysteresis"]["high"]["reset"]["humidity"]), num(data["hysteresis"]["low"]["send"]["humidity"]) ,highest]


instemp = 6 #initialize region value

for i in range(5):
    ins_low = inspect_temp[i]
    ins_high = inspect_temp[i+1]
    #
    if ins_low<nowtemp and ins_high>nowtemp:
        instemp = i

inshum = 6 #initialize region value

i = 6

for i in range(5):
    ins_low = inspect_hum[i]
    ins_high = inspect_hum[i+1]
    #
    if ins_low<nowhum and ins_high>nowhum:
        inshum = i

#===================================================#
#data comparision (nowdata, loggeddata)

##temperature

templog_status = [0,0,0,0,0,0] #High Low 시작, 종료, 지속, Low Log 시작, 종료, 지속

if data["log"]["status"]["temperature"] == "high" and (instemp in [1]):
    # 이전 상태가 HIGH LOGGING 상태이면서, 현태 상태가 LOW 인 경우
    # HIGH LOGGING 을 중단하고, LOW LOGGING 을 시작함
    templog_status = [0,1,0,1,0,0]
elif data["log"]["status"]["temperature"] == "high" and (instemp in [2,3]):
    # 이전 상태가 HIGH LOGGING 상태이면서, 현태 상태가 Normal 인 경우
    # HIGH LOGGING 을 중단함.
    templog_status = [0,1,0,0,0,0]
elif data["log"]["status"]["temperature"] == "high" and (instemp in [4,5]):
    # 이전 상태가 HIGH LOGGING 상태이면서, 현태 상태가 High Hyst 또는 High 인 경우
    # HIGH LOGGING 을 계속함.
    templog_status = [0,0,1,0,0,0]
elif data["log"]["status"]["temperature"] == "normal" and (instemp in [1]):
    # 이전 상태가 normal_unlogging 상태이면서, 현태 상태가 Low 인 경우
    # LOGGING을 시작함 (Low)
    templog_status = [0,0,0,1,0,0]
elif data["log"]["status"]["temperature"] == "normal" and (instemp in [2,3,4]):
    # 이전 상태가 normal_unlogging 상태이면서, 현태 상태가 Normal, High Hyst, Low Hyst 인 경우
    # LOGGING 을 안하고 있는 것을 지속함.
    templog_status = [0,0,0,0,0,0]
elif data["log"]["status"]["temperature"] == "normal" and (instemp in [5]):
    # 이전 상태가  normal_unlogging 상태이면서, 현태 상태가 High 인 경우
    # HIGH LOGGING 을 시작함 (High)
    templog_status = [1,0,0,0,0,0]
elif data["log"]["status"]["temperature"] == "low" and (instemp in [1,2]):
    # 이전 상태가 LOW LOGGING 상태이면서, 현태 상태가 Low, Low Hyst 인 경우
    # LOW LOGGING 을 계속함.
    templog_status = [0,0,0,0,0,1]
elif data["log"]["status"]["temperature"] == "low" and (instemp in [3,4]):
    # 이전 상태가 LOW LOGGING 상태이면서, 현태 상태가 Normal, High Hyst 인 경우
    # LOW LOGGING 을 중단함.
    templog_status = [0,0,0,0,0,0]
elif data["log"]["status"]["temperature"] == "low" and (instemp in [5]):
    # 이전 상태가 LOW LOGGING 상태이면서, 현태 상태가 High 인 경우
    # LOW LOGGING 을 중단하고, HIGH LOGGING 을 시작함.
    templog_status = [1,0,0,0,1,0]

##humidity

humlog_status = [0,0,0,0,0,0] #High Low 시작, 종료, 지속, Low Log 시작, 종료, 지속

if data["log"]["status"]["humidity"] == "high" and (inshum in [1]):
    # 이전 상태가 HIGH LOGGING 상태이면서, 현태 상태가 LOW 인 경우
    # HIGH LOGGING 을 중단하고, LOW LOGGING 을 시작함
    humlog_status = [0,1,0,1,0,0]
elif data["log"]["status"]["humidity"] == "high" and (inshum in [2,3]):
    # 이전 상태가 HIGH LOGGING 상태이면서, 현태 상태가 Normal 인 경우
    # HIGH LOGGING 을 중단함.
    humlog_status = [0,1,0,0,0,0]
elif data["log"]["status"]["humidity"] == "high" and (inshum in [4,5]):
    # 이전 상태가 HIGH LOGGING 상태이면서, 현태 상태가 High Hyst 또는 High 인 경우
    # HIGH LOGGING 을 계속함.
    humlog_status = [0,0,1,0,0,0]
elif data["log"]["status"]["humidity"] == "normal" and (inshum in [1]):
    # 이전 상태가 normal_unlogging 상태이면서, 현태 상태가 Low 인 경우
    # LOGGING을 시작함 (Low)
    humlog_status = [0,0,0,1,0,0]
elif data["log"]["status"]["humidity"] == "normal" and (inshum in [2,3,4]):
    # 이전 상태가 normal_unlogging 상태이면서, 현태 상태가 Normal, High Hyst, Low Hyst 인 경우
    # LOGGING 을 안하고 있는 것을 지속함.
    humlog_status = [0,0,0,0,0,0]
elif data["log"]["status"]["humidity"] == "normal" and (inshum in [5]):
    # 이전 상태가  normal_unlogging 상태이면서, 현태 상태가 High 인 경우
    # HIGH LOGGING 을 시작함 (High)
    humlog_status = [1,0,0,0,0,0]
elif data["log"]["status"]["humidity"] == "low" and (inshum in [1,2]):
    # 이전 상태가 LOW LOGGING 상태이면서, 현태 상태가 Low, Low Hyst 인 경우
    # LOW LOGGING 을 계속함.
    humlog_status = [0,0,0,0,0,1]
elif data["log"]["status"]["humidity"] == "low" and (inshum in [3,4]):
    # 이전 상태가 LOW LOGGING 상태이면서, 현태 상태가 Normal, High Hyst 인 경우
    # LOW LOGGING 을 중단함.
    humlog_status = [0,0,0,0,0,0]
elif data["log"]["status"]["humidity"] == "low" and (inshum in [5]):
    # 이전 상태가 LOW LOGGING 상태이면서, 현태 상태가 High 인 경우
    # LOW LOGGING 을 중단하고, HIGH LOGGING 을 시작함.
    #



