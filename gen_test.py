from gen_alarm import Alarm
from gen_song import Song
from gen_timer import Timer
import random
import argparse

# def export(arr):
#     f_in = open("f_in.txt","w",encoding="utf-8")
#     for i in range(len(arr)):
#         temp = ""
#         w,t,l = arr[i]
#         for word,tag in zip(w.split(),t.split()):
#             temp = temp +word+':'+tag+' '
#         temp = temp +l
#         f_in.write(temp+'\n')

#     f_in.close()

def export(arr):
    f_in = open("seq.in","w",encoding="utf-8")
    f_out = open("seq.out","w",encoding="utf-8")
    f_label = open("label","w",encoding="utf-8")
    random.shuffle(arr)
    for i in range(len(arr)):
        temp = ""
        w,t,l = arr[i]
        # for word,tag in zip(w.split(),t.split()):
        #     temp = temp +word+':'+tag+' '
        # temp = temp +l
        f_in.write(w+'\n')
        f_out.write(t+'\n')
        f_label.write(l+'\n')

    f_in.close()
    f_out.close()
    f_label.close()
def main(args):
    t = Timer()
    s = Song()
    a = Alarm()

    arr = []
    n  = args.n
    while(n>0):
        num_gens = random.randint(1,int(n/2)) if int(n/2) > 1 else 1
        j = random.randint(0,2)
        if(j==0):
            a.genBase(num_gens,arr)
        elif j==1:
            t.genBase(num_gens,arr)
        elif j==2:
            s.genBase(num_gens,arr)
        else:
            return

        n = n-num_gens
    
    export(arr)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--self.fill',type=str,required=True)
    # parser.add_argument('--pattern',type=str,required=True)
    parser.add_argument('--n',type=int,default=100)
    args = parser.parse_args()
    main(args)