import random
import string
import pandas as pd

class Alarm():
    def __init__(self):
        self.f_in = open("alarm_in.txt","a",encoding="utf-8")
        self.f_out = open("alarm_out.txt","a",encoding="utf-8")
        self.pattern_file = pd.read_excel("others.xlsx")
        self.filler = pd.read_excel("datetime.xlsx")

    def genBase(self,n,arr = None):
        pattern_file = self.pattern_file
        song = self.filler
        s1 = pd.Series(pattern_file['s1']).dropna()
        s2 = pd.Series(pattern_file['s2']).dropna()
        s3 = pd.Series(pattern_file['s3']).dropna()
        e1 = pd.Series(pattern_file['e1']).dropna()
        a1 = pd.Series(pattern_file['a1']).dropna()
        b1 = pd.Series(pattern_file['b1']).dropna()
        c1 = pd.Series(pattern_file['c1']).dropna()
        d1 = pd.Series(pattern_file['d1']).dropna()
        pattern = pd.Series(pattern_file['pattern']).dropna()
        # print(pattern)

        for i in range(n):
            s = pattern[random.randint(0,len(pattern)-1)]  
            s = s.replace(" + ", " ").replace("  "," ")
            s = s.replace(" + ", " ").replace("  "," ")
            s = s.replace(" + ", " ").replace("  "," ")
            
            s,t = self.fit(s,song)
            
            sr,tr = s,t
            s,t = self.fill(s,t,"s1",s1[random.randint(0,len(s1)-1)])
            s,t = self.fill(s,t,"s2", s2[random.randint(0,len(s2)-1)])
            s,t = self.fill(s,t,"s3", s3[random.randint(0,len(s3)-1)])
            s,t = self.fill(s,t,"e1", e1[random.randint(0,len(e1)-1)])
            s,t = self.fill(s,t,"a1", a1[random.randint(0,len(a1)-1)])
            s,t = self.fill(s,t,"b1", b1[random.randint(0,len(b1)-1)])
            s,t = self.fill(s,t,"c1", c1[random.randint(0,len(c1)-1)],"repeat")
            s,t = self.fill(s,t,"d1", d1[random.randint(0,len(d1)-1)],"repeat")

            
            
            # print(s)
            # print(t)
            if arr != -1:
                arr.append((s,t,'alarm'))
            else:
                self.f_in.write(s+'\n')
                self.f_out.write(t+'\n')

        self.f_in.close()
        self.f_out.close() 

    def fit(self,s, song):
        t =s
        copy = s
        # print(t)
        name = pd.Series(song['date_name']).dropna()
        month = pd.Series(song['month_name']).dropna()
        num = pd.Series(song['day_number'],dtype=str).dropna()
        pod = pd.Series(song['pod']).dropna()
        relative = pd.Series(song['relative']).dropna()
        week = pd.Series(song['week']).dropna()
        i = random.randint(0,len(name)-1)

        s,t = self.fill(s,t,"date_name", name[random.randint(0,len(name)-1)],type = "date_name")
        s,t = self.fill(s,t,"date_number", num[random.randint(0,len(num)-1)],type = "date_number")
        s,t = self.fill(s,t,"month", month[random.randint(0,len(month)-1)],type = "month")
        s,t = self.fill(s,t,"pod", pod[random.randint(0,len(pod)-1)],type = "pod")
        s,t = self.fill(s,t,"relative", relative[random.randint(0,len(relative)-1)],type = "relative")
        s,t = self.fill(s,t,"week", week[random.randint(0,len(week)-1)],type = "relative")
        # s,t = self.fill(s,t,"c1", c1[random.randint(0,len(c1)-1)])
        # s,t = self.fill(s,t,"d1", d1[random.randint(0,len(d1)-1)])

        s,t = self.fillTime(s,t)
        return s,t

    def fill(self,s,t, base, val, type = ""):
        # print("v: ",val)
        if base not in s:
            return s,t
        if base==None or val == None or val == "" :
            return s,t
        if val == "NONE":
            return s + "NONE",t
        # if base == "pod":
        #     print(s,t,val, len(val.split()))
        temp = ""
        # if(base == "e1"):
        #     print("S:",val)
        val_count = len(val.split())
        s = s.replace(base,val)
        s = s.replace("?",str(random.randint(2,10)))
        if(type == ""):
            temp = "O"
            for i in range(1,val_count):
                temp = temp + " O" 
            t = t.replace(base, temp)

        else:
            temp = "B-" + type
            for i in range(1,val_count):
                temp = temp + " I-" + type
            t = t.replace(base, temp)


        return s,t

    def fillTime(self,s,t):
        fs = ""
        i = random.randint(0,2)
        if(i==0):
            fs = str(random.randint(0,24)) + " giờ"
        elif(i==1):
            a =  random.randint(0,59)
            fs = str(random.randint(0,23)) + ":" 
            if(a<9):
                fs = fs + '0' + str(a)
            else:
                fs = fs + str(a)

        else:
            min = [":15",":30",":45",":00"]
            fs = str(random.randint(0,23)) + min[random.randint(0,2)]
        s,t = self.fill(s,t,"time",fs,"time")
        return s,t