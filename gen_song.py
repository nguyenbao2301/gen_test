import argparse
from http.client import SWITCHING_PROTOCOLS
import random
import pandas as pd


class Song():
    def __init__(self):
        self.f_in = open("song_in.txt","a",encoding="utf-8")
        self.f_out = open("song_out.txt","a",encoding="utf-8")
        self.pattern_file = pd.read_excel("song_pattern.xlsx")
        self.filler = pd.read_excel("song_list.xlsx")

    def genBase(self,n,arr = -1):
        pattern_file = self.pattern_file
        song = self.filler

        s1 = pd.Series(pattern_file['s1']).dropna()
        s2 = pd.Series(pattern_file['s2']).dropna()
        s3 = pd.Series(pattern_file['s3']).dropna()
        a1 = pd.Series(pattern_file['a1']).dropna()
        b1 = pd.Series(pattern_file['b1']).dropna()
        c1 = pd.Series(pattern_file['c1']).dropna()
        d1 = pd.Series(pattern_file['d1']).dropna()
        pattern = pd.Series(pattern_file['pattern']).dropna()
        # print(pattern)

        for i in range(n):
            s = pattern[random.randint(0,len(pattern)-1)]  
            s,t = self.fit(s,song)
            
        
            s,t = self.fill(s,t,"s1", s1[random.randint(0,len(s1)-1)])
            s,t = self.fill(s,t,"s2", s2[random.randint(0,len(s2)-1)])
            s,t = self.fill(s,t,"s3", s3[random.randint(0,len(s3)-1)])
            s,t = self.fill(s,t,"a1", a1[random.randint(0,len(a1)-1)])
            s,t = self.fill(s,t,"b1", b1[random.randint(0,len(b1)-1)])
            s,t = self.fill(s,t,"c1", c1[random.randint(0,len(c1)-1)])
            s,t = self.fill(s,t,"d1", d1[random.randint(0,len(d1)-1)])

            
            s = s.replace(" + ", " ").replace("  "," ")
            s = s.replace(" + ", " ").replace("  "," ")
            s = s.replace(" + ", " ").replace("  "," ")
            t = t.replace(" + ", " ").replace("  "," ")
            # # print(s)
            # # print(t)
            if arr != -1:
                arr.append((s,t,'play_song'))
            else:
                self.f_in.write(s+'\n')
                self.f_out.write(t+'\n')

        self.f_in.close()
        self.f_out.close()    


    def fit(self,s, song):
        t =s
        copy = s
        # print(t)
        name = pd.Series(song['name'])
        album = pd.Series(song['album'])
        a1 = pd.Series(song['artist'])
        a2 = pd.Series(song['artist_2'])
        genre = pd.Series(song['genre']).dropna()
        i = random.randint(0,len(name)-1)

        s,t = self.fill(s,t,'song_name', name[i],"song_name")
        s,t = self.fill(s,t,'album', album[i] if album.notna()[i] else 'NONE',"album")
        s,t = self.fill(s,t,'artist_1', a1[i] if a1.notna()[i] else 'NONE',"artist")
        s,t = self.fill(s,t,'artist_2', a2[i] if a2.notna()[i] else 'NONE',"artist")
        
        s,t = self.fill(s,t,'genre', genre[random.randint(0,len(genre)-1)],"genre" )

        if "NONE" in s:
            return self.fit(copy,song)
        return s,t

    def fill(self,s,t, base, val, type = ""):
        # print("s: ",s)
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

def main(args):
    s = Song()
    s.genBase(args.n)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--self.fill',type=str,default="./song_list.xlsx")
    # parser.add_argument('--pattern',type=str,default="./song_pattern.xlsx")
    parser.add_argument('--n',type=int,default=100)
    args = parser.parse_args()
    main(args)