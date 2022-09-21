import argparse
from http.client import SWITCHING_PROTOCOLS
import random
import string
import pandas as pd

class Timer():
    def __init__(self):
        self.f_in = open("timer_in.txt","a",encoding="utf-8")
        self.f_out = open("timer_out.txt","a",encoding="utf-8")
        self.pattern_file = pd.read_excel("timer.xlsx")
        self.filler = pd.read_excel("datetime.xlsx")

    def genBase(self,n,arr=-1):
        s1 = pd.Series(self.pattern_file['s1']).dropna()
        s2 = pd.Series(self.pattern_file['s2']).dropna()
        s3 = pd.Series(self.pattern_file['s3']).dropna()
        hour = pd.Series(self.pattern_file['hour']).dropna()
        minute = pd.Series(self.pattern_file['minute']).dropna()
        second = pd.Series(self.pattern_file['second']).dropna()
        c1 = pd.Series(self.pattern_file['c1']).dropna()
        d1 = pd.Series(self.pattern_file['d1']).dropna()
        pattern = pd.Series(self.pattern_file['pattern']).dropna()
        # print(pattern)

        for i in range(n):
            s = pattern[random.randint(0,len(pattern)-1)]  
            s,t = self.fit(s)
            
        
            s,t = self.fill(s,t,"s1", s1[random.randint(0,len(s1)-1)])
            s,t = self.fill(s,t,"s2", s2[random.randint(0,len(s2)-1)])
            s,t = self.fill(s,t,"s3", s3[random.randint(0,len(s3)-1)])
            s,t = self.fill(s,t,"hour", hour[random.randint(0,len(hour)-1)],"hour")
            s,t = self.fill(s,t,"minute", minute[random.randint(0,len(minute)-1)],"minute")
            s,t = self.fill(s,t,"second", second[random.randint(0,len(second)-1)],"second")
            s,t = self.fill(s,t,"c1", c1[random.randint(0,len(c1)-1)])
            s,t = self.fill(s,t,"d1", d1[random.randint(0,len(d1)-1)])

            s,t = self.fill(s,t,"và", "và")
            s,t = self.fill(s,t,"phút", "phút")
            
            s = s.replace(" + ", " ").replace("  "," ")
            s = s.replace(" + ", " ").replace("  "," ")
            s = s.replace(" + ", " ").replace("  "," ")
            t = t.replace(" + ", " ").replace("  "," ")
            # print(s)
            # print(t)
            if arr != -1:
                arr.append((s,t,'timer'))
            else:
                self.f_in.write(s+'\n')
                self.f_out.write(t+'\n')

        self.f_in.close()
        self.f_out.close()    

    def fit(self,s):
        t =s
        s,t = self.fillTime(s,t)
        return s,t

    def fill(self,s,t, base, val, type = ""):
        # print("v: ",val)
        
        if base==None or val == None :
            return s,t
        if val == "NONE":
            return s + "NONE",t
        temp = ""
        val_count = len(val.split())
        s = s.replace(base,val)
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
            fs = str(random.randint(0,23)) + ":" + str(random.randint(0,59))
        else:
            min = [":15",":30",":45"]
            fs = str(random.randint(0,23)) + min[random.randint(0,2)]
        s,t = self.fill(s,t,"time",fs,"time")
        return s,t
def main(args):
    t = Timer()
    t.genBase(args.n)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--n',type=int,default=100)
    args = parser.parse_args()
    main(args)