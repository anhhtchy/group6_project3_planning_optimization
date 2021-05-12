from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('CBC') #MIP
print('create solver OK')

INF = solver.infinity()

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

N, K, w, l, W, L, c = input('./test-data-1.txt')
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

# variables
x1 = [solver.IntVar(0, max_W, 'x1('+str(i)+')') for i in range(N)]
y1 = [solver.IntVar(0, max_L, 'y1('+str(i)+')') for i in range(N)]
o  = [solver.IntVar(0, 1, 'o('+str(i)+')') for i in range(N)]
p  = [solver.IntVar(0, K-1, 'p('+str(i)+')') for i in range(N)]
# extra variables
x2 = [solver.IntVar(0, max_W, 'x2('+str(i)+')') for i in range(N)]
y2 = [solver.IntVar(0, max_L, 'y2('+str(i)+')') for i in range(N)]

for i in range(N):
    constraint_x = solver.Constraint(l[i], l[i])
    constraint_x.SetCoefficient(x1[i], -1)
    constraint_x.SetCoefficient(x2[i], 1)
    constraint_x.SetCoefficient(o[i], l[i]-w[i])

    constraint_y = solver.Constraint(w[i], w[i])
    constraint_y.SetCoefficient(y1[i], -1)
    constraint_y.SetCoefficient(y2[i], 1)
    constraint_y.SetCoefficient(o[i], w[i]-l[i])

for i in range(N):
    for j in range(K):
        # pass
        solver.Add(INF*(p[i]-j) + x2[i] <= W[j])
        solver.Add(INF*(p[i]-j) + y2[i] <= L[j])
        # constraint_x = solver.Constraint(0, W[j]+j*INF)
        # constraint_x.SetCoefficient(x2[i], 1)
        # constraint_x.SetCoefficient(p[i], INF)

        # constraint_y = solver.Constraint(0, L[j]+j*INF)
        # constraint_y.SetCoefficient(y2[i], 1)
        # constraint_y.SetCoefficient(p[i], INF)
        

p_ = [[solver.IntVar(0, 1, 'p_('+str(i)+','+str(j)+')') for j in range(K)] for i in range(N)]
# for i in range(N):
#     for j in range(K):
#         constraint1 = solver.Constraint(1+INF*j, 1+INF*j)
#         constraint1.SetCoefficient(p[i], INF)
#         constraint1.SetCoefficient(p_[i][j], 1)

#         constraint2 = solver.Constraint(j-INF, j-INF)
#         constraint2.SetCoefficient(p[i], 1)
#         constraint2.SetCoefficient(p_[i][j], -INF)

u  = [solver.IntVar(0, 1, 'u('+str(j)+')') for j in range(K)]
# for j in range(K):
#     constraint1 = solver.Constraint(-N, 0)
#     constraint1.SetCoefficient(u[j], 1)
#     for i in range(N):
#         constraint1.SetCoefficient(p_[i][j], -1)
#         constraint2 = solver.Constraint(0, 1)
#         constraint2.SetCoefficient(u[j], 1)
#         constraint2.SetCoefficient(p_[i][j], -1)

e = [[[solver.IntVar(0, 1, 'e('+str(m)+','+str(n)+','+str(k)+')') for k in range(4)] for n in range(N)] for m in range(N)]
# for m in range(N):
#     for n in range(N):
#         constraint1 = solver.Constraint(-INF, 0)
#         constraint1.SetCoefficient(p[m], INF)
#         constraint1.SetCoefficient(p[n], -INF)
#         constraint1.SetCoefficient(x2[m], 1)
#         constraint1.SetCoefficient(x1[n], -1)
#         constraint1.SetCoefficient(e[m][n][0], -INF)

#         constraint2 = solver.Constraint(-INF, 0)
#         constraint2.SetCoefficient(p[m], INF)
#         constraint2.SetCoefficient(p[n], -INF)
#         constraint2.SetCoefficient(x2[n], 1)
#         constraint2.SetCoefficient(x1[m], -1)
#         constraint2.SetCoefficient(e[m][n][1], -INF)

#         constraint3 = solver.Constraint(-INF, 0)
#         constraint3.SetCoefficient(p[m], INF)
#         constraint3.SetCoefficient(p[n], -INF)
#         constraint3.SetCoefficient(y2[m], 1)
#         constraint3.SetCoefficient(y1[n], -1)
#         constraint3.SetCoefficient(e[m][n][2], -INF)

#         constraint4 = solver.Constraint(-INF, 0)
#         constraint4.SetCoefficient(p[m], INF)
#         constraint4.SetCoefficient(p[n], -INF)
#         constraint4.SetCoefficient(y2[n], 1)
#         constraint4.SetCoefficient(y1[m], -1)
#         constraint4.SetCoefficient(e[m][n][3], -INF)

#         constraint5 = solver.Constraint(0, 3)
#         for k in range(4):
#             constraint5.SetCoefficient(e[m][n][k], 1)
        
obj = solver.Objective()
for j in range(K):
    obj.SetCoefficient(u[j], c[j])
obj.SetMinimization()

result_status = solver.Solve()

if result_status == pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
elif result_status == pywraplp.Solver.INFEASIBLE:
    print('INFEASIBLE')
elif result_status == pywraplp.Solver.NOT_SOLVED:
    print('NOT_SOLVED')    