import random

def genData(fileName, nTrucks):
    K = nTrucks
    N = random.randrange(round(1.5*K), 2*K)
    minWL = 20
    maxWL = 40
    f = open(fileName, 'w')
    f.write(str(N) + ' ' + str(K) + '\n')
    for i in range(round(N/3)):
        w_i = random.randrange(1, minWL)
        l_i = random.randrange(1, minWL)
        f.write(str(w_i) + ' ' + str(l_i) + '\n')
    for i in range(N-round(N/3)):
        w_i = random.randrange(1, round(minWL/2))
        l_i = random.randrange(1, round(minWL/2))
        f.write(str(w_i) + ' ' + str(l_i) + '\n')
    for i in range(K):
        W_i = random.randrange(minWL, maxWL)
        L_i = random.randrange(minWL, maxWL)
        c_i = W_i*L_i
        f.write(str(W_i) + ' ' + str(L_i) + ' ' + str(c_i) + '\n')
    f.close()

nTrucks = 37
genData("data/data_{}.txt".format(nTrucks), nTrucks)