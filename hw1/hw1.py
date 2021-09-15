
def PV_YTM(s, C, n, w):
    pv = 0
    for i in range(n):
        pv = pv + C[i] / ((1+s[i])**(i+w))

    accuracy = 1000000
    minErr = 99999999
    bestY = 1/accuracy
    for y in range(accuracy):
        Yield = (y+1.0)/accuracy + 1
        err = 0
        for i in range(n):
            err = err + C[i]/(Yield**(w+i))
        err = abs(pv-err)
        if(err < minErr):
            minErr = err
            bestY = Yield - 1

    return pv, bestY

def MD(s, C, n, w):
    pv, y = PV_YTM(s, C, n, w)    
    
    duration = 0
    for i in range(n):
        duration += C[i]*(i+w)/(1+s[i])**(i+w)
    duration = duration / pv / (1+y)

    return duration

def Convexity(s, C, n, w):
    pv, y = PV_YTM(s, C, n, w)
    conv = 0
    for i in range(n):
        conv += C[i]*(w+i+1)*(w+i) / ((1+s[i])**(w+i+2))
    conv = conv / pv
    return conv

if __name__ == '__main__':
    # input start
    C = [3, 2, 3, 2, 103]
    s = [0.053, 0.051, 0.049, 0.047, 0.040]
    # input end
    w = 1
    n = len(s)

    duration = MD(s, C, n, w)
    convexity = Convexity(s, C, n, w)
    print("modified duration: %.4f\nconvexity: %.4f" % (duration, convexity/100))
