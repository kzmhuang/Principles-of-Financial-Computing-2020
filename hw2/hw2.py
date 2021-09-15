import sys
import math
import string

# read input
def read_input(file_path="input.txt"):
    with open(file_path, 'r') as f:
        S = float(f.readline()) # stock price
        X = float(f.readline()) # strike price
        r = float(f.readline().replace("%",""))/100
        s = float(f.readline().replace("%",""))/100 # var
        T = int(f.readline())
        Estr = f.readline().replace("[","").replace("]","")
        E = [float(i.strip()) for i in Estr.split(",")]
        m = float(f.readline())
    # print(S,X,r,s,T,E,m)
    return(S,X,r,s,T,E,m)

def Bermuda_put(S,X,r,s,T,E,m):
    # variable
    mature = T
    holiday = 0
    trading = mature - holiday #可交易的天數

    T = int(trading*m)
    N = int(mature*m)
    trading = float(trading)
    R = math.exp(r*(1/(365*m))) #每期 利率折現
    u = math.exp(s*((1/(365*m))**(0.5))) # 261:股市交易天數
    d = 1/u
    q = (R-d)/(u-d)
    # print(mature, N)
    # exit()
    #option pricing
    option_price = []
    stock_price = []
    #put
    for i in range(0, T + 1):
        stock_price.append(S * u**(T-i) * d**i) # S(T)
        option_price.append(max(0, X - stock_price[i])) # C(T) 已包含最後一天可履行

    for i in range(0, N):
        day = (i // m) + 1
        for j in range(0, T):
            stock_price[j] = stock_price[j] / u
            if(day in E or day == mature): # excercise day: 當天每個節點都算
                option_price[j] = max((option_price[j]*q + option_price[j+1]*(1-q)) / R, X - stock_price[j]) # 原本有/R
            else:
                option_price[j] = (option_price[j]*q + option_price[j+1]*(1-q)) / R
        # print(day)
    return option_price[0]

if __name__ == '__main__':
    S, X, r, s, T, E, m = read_input()
    # exit()
    put_price = Bermuda_put(S,X,r,s,T,E,m)
    print(put_price)
    print("put price of Bermuda option: %.4f" % (put_price))


