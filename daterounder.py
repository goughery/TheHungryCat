import datetime

def roundDate(t):
    #t = datetime.datetime.now()
    if t.minute <= 15:
        return t.replace(second = 0, microsecond = 0, minute = 0, hour = t.hour)
    elif t.minute > 15 and t.minute <= 45:
        return t.replace(second = 0, microsecond = 0, minute = 30, hour = t.hour)
    else:
        return t.replace(second = 0, microsecond = 0, minute = 0, hour = t.hour + 1)
    

date = datetime.datetime.now() - datetime.timedelta(hours = 24, minutes = 30)

datenow = datetime.datetime.now()

print(date - datenow)
#date = date.replace(second = 0, microsecond = 0, minute = 32, hour = date.hour)

print(roundDate(date))
