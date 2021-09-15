'''
Inputs: 
        x (year), 
        y (year), 
        r (%) (initial short rate), 
        b (%) and 
        m (%), 
        s (%), 
        n (the number of steps during the option's life), and 
        strike price X (% of par).
'''

import sys
from math import *
import numpy as np

def treeCIR(x, y, r, b, m, s, n, X):

    # Initial value
    t = x
    T = y
    r = r / 100
    b = b / 100  # from percentage to decimal
    m = m / 100
    s = s / 100
    n = n
    X = X / 100

    # data after calc
    deltaT = T/n
    #print "deltaT = "+str(deltaT)
    x_r = 2*sqrt(r)/s
    deltaX = sqrt(deltaT)
    optionDuration = n*t/T
    gamma = sqrt(b*b + 2*s*s)
        
    #print optionDuration
    # Initial Price
    Price = np.ones(n+1)
    Option = np.zeros((n+1, n+1))
    # Binomial CIR model
    transformToOption = False
    tt = T

    # option price at maturity
    for i in range(n+1):
        x_prime = x_r + (n - 2*i) * deltaX
        r_prime = x_prime**2 * s**2 / 4

        c1 = gamma
        c2 = (b + c1) / 2
        c3 = 2 * b * m / s ** 2
        tmp = exp(c1*(T-tt))-1

        # A = pow((2*gamma*exp((b+gamma)*(T-tt)/2) / ((b+gamma)*tmp+2*gamma)), 2*b*m/s/s)
        # B = 2*tmp / ((b+gamma)*tmp+2*gamma)
        A = pow((c1 * exp(c2 * (T-tt)) / (c2 * tmp + c1)), c3)
        B = tmp / (c2 * tmp + c1)           
        Price[i] = 1.0 * A * exp(-B*m)
        # print(X, Price[i])
        Option[n][i] = max(X-Price[i], 0)


    for j in reversed(range(n)):

        tt = tt - deltaT
        for i in range(j+1):
            # CIR
            p = 1
            x_prime = x_r + (j - 2*i) * deltaX
            r_prime = x_prime**2 * s**2 / 4

            r_plus = (x_prime + deltaX)**2 * s**2 / 4
            r_minus = (x_prime - deltaX)**2 * s**2 / 4
            p = (b*(m-r_prime) * deltaT + r_prime - r_minus) / (r_plus-r_minus)

            if p<0: 
                p=0
            elif p>1:
                p=1
            # CIR end

            discountFactor = 1 / exp(r_prime * deltaT) # r_prime?
            #print "dis = "+str(discountFactor)
            #Price[i] = (p*Price[i]+(1.0-p)*Price[i+1])*discountFactor
            c1 = gamma
            c2 = (b + c1) / 2
            c3 = 2 * b * m / s ** 2
            tmp = exp(c1*(T-tt))-1

            # A = pow((2*gamma*exp((b+gamma)*(T-tt)/2) / ((b+gamma)*tmp+2*gamma)), 2*b*m/s/s)
            # B = 2*tmp / ((b+gamma)*tmp+2*gamma)
            A = pow((c1 * exp(c2 * (T-tt)) / (c2 * tmp + c1)), c3)
            B = tmp / (c2 * tmp + c1)           
            Price[i] = 1.0 * A * exp(-B*r_prime)
            # print(i, j, Price[i])
            cont = (p*Option[j+1][i] + (1.0-p)*Option[j+1][i+1]) * discountFactor
            if (j <= optionDuration): # exercise
                Option[j][i] = max(X-Price[i], cont, 0)
            else:
                # print(j)
                Option[j][i] = max(cont, 0)

            # print(Option[j][i])
            # print(i, j, Option[j][i])
    return 100*(Option[0][0])



if __name__ == "__main__":
    #python3 hw4.py 1 3 1 30 2 30 150 95
    
    # input
    x = float(sys.argv[1])
    y = float(sys.argv[2])
    r = float(sys.argv[3])
    b = float(sys.argv[4])
    m = float(sys.argv[5])
    s = float(sys.argv[6])
    n = int(sys.argv[7])
    X = float(sys.argv[8])

    price = treeCIR(x, y, r, b, m, s, n, X)
    print('%.4f' % (price))
