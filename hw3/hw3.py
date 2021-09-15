import math
import numpy as np
import sys

def AmericanStyle_AsianPut(Spot, sigma, n, m, Strike, r, nT, H):

    T = nT / n
    priceMatrix = np.zeros((m, n))
    for i in range(m):
        priceMatrix[i, :] = Spot * np.exp(
            np.cumsum(
                (r - 0.5 * sigma ** 2) * T
                + (sigma * math.sqrt(T) * np.random.normal(0, 1, n))
            )
        )

    # Asian
    meanMatrix = np.concatenate((np.reshape(priceMatrix[:, 0], (m, -1)), np.zeros((m, n - 1))), axis=1)
    for i in range(1, n):
        meanMatrix[:, i] = np.mean(priceMatrix[:, :i + 1], axis=1)


    diffMatrix = np.maximum(0, Strike - meanMatrix)
    # up-and-out
    for i in range(m):
        idx = np.where(meanMatrix[i, :] >= H)
        # print(idx)
        if(len(idx[0]) > 0):
            # print(idx)
            diffMatrix[i, idx[0][0]:] = 0
            # print(diffMatrix[i, idx[0][0]:])

    # X = np.where(diffMatrix > 0, priceMatrix, 0)
    X = np.where(diffMatrix > 0, meanMatrix, 0)    
    Xsh = X[:, :-1]
    # print(X.shape, Xsh.shape)
    # exit()
    Y1 = diffMatrix * math.exp(-r * T)
    Y2 = np.concatenate((np.zeros((m, n - 1)), np.vstack(Y1[:, n - 1])), axis=1)
    CV = np.zeros((m, n - 1))


    # print("start poly")
    # iteration
    for i in range(n - 2, -1, -1):
        degree = 3
        # print(len(Xsh[:, i]), len(Y2[:, i + 1]))
        reg1 = np.polyfit(Xsh[:, i], Y2[:, i + 1], degree)
        for d in range(degree + 1):
            CV[:, i] += reg1[-d - 1] * Xsh[:, i] ** d
            # CV[:, i] = reg1[2] + reg1[1] * Xsh[:,i] + reg1[0] * (Xsh[:,i] ** 2)

        CV[:, i] = np.nan_to_num(CV[:, i])
        Y2[:, i] = np.where(diffMatrix[:, i] > CV[:, i], Y1[:, i], Y2[:, i + 1] * math.exp(-r * T))

    CV = np.nan_to_num(CV)
    CVp = np.concatenate((CV, np.zeros((m, 1))), axis=1)
    pofMatrix = np.where(CVp > diffMatrix, 0, diffMatrix)

    # print("end poly")
    # first value row
    M = np.zeros((m,n))
    for i in range(m):
        M[i, :] = np.cumsum(pofMatrix[i, :])
    M2 = np.concatenate((np.zeros((m, 1)), M[:, :-1]), axis=1)
    fpofMatrix = np.zeros((m, n))
    for i in range(pofMatrix.shape[1]):
        fpofMatrix[:, i] = np.where(M2[:, i] > 0, 0, pofMatrix[:, i])

    dfpofMatrix = np.zeros((m, n))
    for i in range(n):
        dfpofMatrix[:, i] = fpofMatrix[:, i] * math.exp(-T * r * (i + 1))
    idx = np.where(dfpofMatrix > 0)
    
    PRICE = np.mean(np.sum(dfpofMatrix, axis=1))
    STD = np.std(np.sum(dfpofMatrix, axis=1)) / (m ** 0.5)
    DEL = math.exp(-r * nT) * np.mean(diffMatrix[:, n-2] -diffMatrix[:, n-1]) # not sure QAQ

    return PRICE, STD, DEL


if __name__ == "__main__":
    #python3 xxx.py 100 100 110 1 0.05 0.30 250 1000000
    
    # input
    S = float(sys.argv[1])
    X = float(sys.argv[2])
    H = float(sys.argv[3])
    T = float(sys.argv[4])
    r = float(sys.argv[5])
    s = float(sys.argv[6])
    n = int(sys.argv[7])
    k = int(sys.argv[8])

    price, std, delta = AmericanStyle_AsianPut(Spot=S, sigma=s, n=n, m=k, Strike=X, r=r, nT=T, H=H)
    print('%.4f %.4f %.4f' % (price, std, delta))
