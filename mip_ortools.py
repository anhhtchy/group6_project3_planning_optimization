from ortools.linear_solver import pywraplp
import time

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

N, K, w, l, W, L, c = input('data/data.txt')
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

solver = pywraplp.Solver.CreateSolver('CBC')
INF = solver.infinity()
M = 100

x1 = [solver.IntVar(0, max_W, 'x1('+str(i)+')') for i in range(N)] 
y1 = [solver.IntVar(0, max_L, 'y1('+str(i)+')') for i in range(N)]
o = [solver.IntVar(0, 1, 'o('+str(i)+')') for i in range(N)]

x2 = [solver.IntVar(0, max_W, 'x2('+str(i)+')') for i in range(N)] 
y2 = [solver.IntVar(0, max_L, 'y2('+str(i)+')') for i in range(N)]
u = [solver.IntVar(0, 1, 'u('+str(i)+')') for i in range(K)]

p = [[solver.IntVar(0, 1, 'p('+str(i)+','+str(j)+')') for j in range(K)] for i in range(N)]
np = [solver.IntVar(0, N, 'np('+str(j)+')') for j in range(K)]
q = [[[[solver.IntVar(0, 1, 'q('+str(i)+','+str(j)+','+str(x)+','+str(y)+')') for y in range(L[j])] for x in range(W[j])] for j in range(K)] for i in range(N)]

for i in range(N):
    c1 = solver.Constraint(1, 1)
    for j in range(K):
        c1.SetCoefficient(p[i][j], 1)
    c2 = solver.Constraint(-l[i], -l[i])
    c2.SetCoefficient(x1[i], 1)
    c2.SetCoefficient(x2[i], -1)
    c2.SetCoefficient(o[i], w[i]-l[i])
    
    c3 = solver.Constraint(-w[i], -w[i])
    c3.SetCoefficient(y1[i], 1)
    c3.SetCoefficient(y2[i], -1)
    c3.SetCoefficient(o[i], l[i]-w[i])

for j in range(K):
    c1 = solver.Constraint(0, 0)
    for i in range(N):
        c1.SetCoefficient(p[i][j], 1)
    c1.SetCoefficient(np[j], -1)

for i in range(N):
    for j in range(K):
        for x in range(W[j]):
            for y in range(L[j]):
                c1 = solver.Constraint(-INF, M-1)
                c1.SetCoefficient(q[i][j][x][y], M)
                c1.SetCoefficient(p[i][j], -1)

                c2 = solver.Constraint(-INF, M+x)
                c2.SetCoefficient(q[i][j][x][y], M)
                c2.SetCoefficient(x1[i], 1)

                c3 = solver.Constraint(-INF, M+y)
                c3.SetCoefficient(q[i][j][x][y], M)
                c3.SetCoefficient(y1[i], 1)

                c4 = solver.Constraint(-INF, M-x-1)
                c4.SetCoefficient(q[i][j][x][y], M)
                c4.SetCoefficient(x2[i], -1)

                c5 = solver.Constraint(-INF, M-y-1)
                c5.SetCoefficient(q[i][j][x][y], M)
                c5.SetCoefficient(y2[i], -1)

for i in range(N):
    c1 = solver.Constraint(w[i]*l[i], w[i]*l[i])
    for j in range(K):
        for x in range(W[j]):
            for y in range(L[j]):
                c1.SetCoefficient(q[i][j][x][y], 1)

for j in range(K):
    for x in range(W[j]):
        for y in range(L[j]):
            c1 = solver.Constraint(0, 1)
            for i in range(N):
                c1.SetCoefficient(q[i][j][x][y], 1)
    
for i in range(N):
    for j in range(K):
        c1 = solver.Constraint(-INF, M-1)
        c1.SetCoefficient(p[i][j], M)
        c1.SetCoefficient(u[j], -1)

        c2 = solver.Constraint(-INF, M+W[j])
        c2.SetCoefficient(p[i][j], M)
        c2.SetCoefficient(x2[i], 1)

        c3 = solver.Constraint(-INF, M+L[j])
        c3.SetCoefficient(p[i][j], M)
        c3.SetCoefficient(y2[i], 1)

for j in range(K):
    c1 = solver.Constraint(-INF, M-1)
    c1.SetCoefficient(u[j], M)
    c1.SetCoefficient(np[j], -1)

obj = solver.Objective()
for j in range(K):
    obj.SetCoefficient(u[j], c[j])

start = time.time()
result_status = solver.Solve()
duration = time.time() - start
if result_status == pywraplp.Solver.OPTIMAL:
    print('Time = {} seconds'.format(duration))
    print('Obj = %i' % solver.Objective().Value())

    for i in range(N):
        for j in range(K):
            if(p[i][j].solution_value()>0):
                print('package {} at truck {}, orientation {}, bottom-left: ({}, {}), top-right: ({}, {})'.format(i, j, \
                    o[i].solution_value(), x1[i].solution_value(), y1[i].solution_value(), x2[i].solution_value(), y2[i].solution_value()))
        