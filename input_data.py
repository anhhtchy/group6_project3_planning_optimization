def input(filename):
    with open(filename, 'r') as f:
        [N, K] = [int(x) for x in f.readline().split()]
        w = [0 for i in range(N)]
        l = [0 for i in range(N)]
        for i in range(N):
            [w[i], l[i]] = [int(x) for x in f.readline().split()]
        W = [0 for i in range(K)]
        L = [0 for i in range(K)]
        c = [0 for i in range(K)]
        for j in range(K):
            [W[j], L[j], c[j]] = [int(x) for x in f.readline().split()]
        return N, K, w, l, W, L, c

N, K, w, l, W, L, c = input('data/data-12.txt')
max_W = max(W)
max_L = max(L)
sum_c = sum(c)

print(N, K)
for i in range(N):
    print('package', i,':', w[i], l[i])
print('========')
for j in range(K):
    print('truck', j,':', W[j], L[j], c[j])
print(max_W, max_L, sum_c)