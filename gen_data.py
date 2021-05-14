import random as rd
def genData(filename, n):
    N = K = n
    minWL = 10
    maxWL = 20
    f = open(filename, 'w')
    f.write(str(N)+' '+str(K)+'\n')
    for i in range(N):
        w_i = rd.randint(1, minWL)
        l_i = rd.randint(1, minWL)
        f.write(str(w_i)+' '+str(l_i)+'\n')
    for j in range(K):
        W_j = rd.randint(minWL, maxWL)
        L_j = rd.randint(minWL, maxWL)
        c_j = 10*(W_j+L_j)
        f.write(str(W_j)+' '+str(L_j)+' '+str(c_j)+'\n')
    f.close()

n = 6
genData('data/data-{}.txt'.format(n), n)
