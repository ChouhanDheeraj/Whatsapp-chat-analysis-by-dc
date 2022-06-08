import pandas as pd
import re
import datetime as dt
def date_time(s):
        pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
        result = re.match(pattern, s)
        if result:
            return True
        else:
            pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
            result = re.match(pattern, s)
            if result:
                return True
            else:
                return False

def getDatapoint(line):
    splitline = line.split(' - ')
    dateTime = splitline[0]
    date, time = dateTime.split(", ")
    message = " ".join(splitline[1:])
    splitmessage = message.split(": ")
    if splitmessage[1:]:
        author = splitmessage[0]
        message = " ".join(splitmessage[1:])
    else:
        author = 'group_notification'
        message = splitmessage[0]
    return date, time, author, message



#df = pd.DataFrame(data, columns=["date", 'time', 'user', 'message'])
def preprosesar(conversations):
    data = []
    conversation = conversations
    with open(conversation, encoding="utf-8") as fp:
        fp.readline()
        messageBuffer = []
        date, time, user = None, None, None
        while True:
            line = fp.readline()
            if not line:
                   break
            line = line.strip()
            if date_time(line):
                if len(messageBuffer) > 0:
                    data.append([date, time, user, ' '.join(messageBuffer)])
                messageBuffer.clear()
                date, time, user, message = getDatapoint(line)
                messageBuffer.append(message)
            else:
                messageBuffer.append(line)
    df = pd.DataFrame(data, columns=["date", 'time', 'user', 'message'])
    df['date'] = pd.to_datetime(df.date, format='%d/%m/%Y')
    df['Year'] = df.date.dt.year
    df['Month'] = df['date'].dt.month_name()
    df['Month_num'] = df['date'].dt.month
    df['Day'] = df.date.dt.day
    df['Time'] = pd.to_datetime(df.time, format='%I:%M %p')
    df['Hours'] = df.Time.dt.hour
    df['Minute']  =df.Time.dt.minute
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    feature = df[['user','message','Year','Month','Day','Hours','Minute','Month_num','only_date','day_name']]
    period = []
    for hour in feature[['day_name','Hours']]['Hours']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str(hour) + '-' + str(hour +1))
        else:
            period.append(str(hour) + '-' + str(hour +1))
    feature['Period']  = period
    return feature
