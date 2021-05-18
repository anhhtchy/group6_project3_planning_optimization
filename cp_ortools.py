from ortools.sat.python import cp_model
import time

def input(filename):
    total_area = 0
    with open(filename, 'r') as f:
        [N, K] = [int(x) for x in f.readline().split()]
        w = [0 for i in range(N)]
        l = [0 for i in range(N)]
        for i in range(N):
            [w[i], l[i]] = [int(x) for x in f.readline().split()]
            total_area += w[i]*l[i]
        W = [0 for i in range(K)]
        L = [0 for i in range(K)]
        c = [0 for i in range(K)]
        for j in range(K):
            [W[j], L[j], c[j]] = [int(x) for x in f.readline().split()]
        return N, K, w, l, W, L, c, total_area

N, K, w, l, W, L, c, total_area = input('data/data.txt')
max_W = max(W)
max_L = max(L)
sum_c = sum(c)

print(N, K)
for i in range(N):
    print('package', i,':', w[i], l[i])
print('========')
for j in range(K):
    print('truck', j,':', W[j], L[j], c[j])
print("max_W: {}, max_L: {}, sum_c: {}, total_area: {}".format(max_W, max_L, sum_c, total_area))

model = cp_model.CpModel()
# variables
x1 = [model.NewIntVar(0,max_W,'x1['+str(i)+']') for i in range(N)]
y1 = [model.NewIntVar(0,max_L,'y1['+str(i)+']') for i in range(N)]
o = [model.NewIntVar(0,1,'o['+str(i)+']') for i in range(N)]
p = [model.NewIntVar(0,K-1,'p['+str(i)+']') for i in range(N)]
# extra variables
x2 = [model.NewIntVar(0,max_W,'x2['+str(i)+']') for i in range(N)]
y2 = [model.NewIntVar(0,max_L,'y2['+str(i)+']') for i in range(N)]
u = [model.NewIntVar(0, 1, 'u['+str(j)+']') for j in range(K)]
# extra variables for modeling in ortools
t = [[model.NewBoolVar('t['+str(i1)+','+str(i2)+']') for i2 in range(N)] for i1 in range(N)]
p_bool = [[model.NewBoolVar('p_bool['+str(i)+','+str(j)+']') for j in range(K)] for i in range(N)]
u_bool = [model.NewBoolVar('u_bool['+str(j)+']') for j in range(K)]

xmn = [[model.NewBoolVar('xmn['+str(i1)+','+str(i2)+']') for i2 in range(N)] for i1 in range(N)]
ymn = [[model.NewBoolVar('ymn['+str(i1)+','+str(i2)+']') for i2 in range(N)] for i1 in range(N)]
xnm = [[model.NewBoolVar('xnm['+str(i1)+','+str(i2)+']') for i2 in range(N)] for i1 in range(N)]
ynm = [[model.NewBoolVar('ynm['+str(i1)+','+str(i2)+']') for i2 in range(N)] for i1 in range(N)]

for j in range(K):
    model.Add(u[j]==1).OnlyEnforceIf(u_bool[j])
    model.Add(u[j]==0).OnlyEnforceIf(u_bool[j].Not())
    # use truck j
    model.AddBoolOr([p_bool[i][j] for i in range(N)]).OnlyEnforceIf(u_bool[j])
    # model.AddBoolAnd([p_bool[i][j].Not() for i in range(N)]).OnlyEnforceIf(u_bool[j].Not())

for i in range(N):
    for j in range(K):
        model.Add(p[i]==j).OnlyEnforceIf(p_bool[i][j])
        model.Add(p[i]!=j).OnlyEnforceIf(p_bool[i][j].Not())
        # constraint: don't put package out of the truck
        model.Add(x2[i]<=W[j]).OnlyEnforceIf(p_bool[i][j])
        model.Add(y2[i]<=L[j]).OnlyEnforceIf(p_bool[i][j])
        # use truck j
        model.Add(u_bool[j]==True).OnlyEnforceIf(p_bool[i][j])

for i in range(N):
    model.Add( x2[i] == x1[i] + o[i]*w[i] - (o[i]-1)*l[i] )
    model.Add( y2[i] == y1[i] + o[i]*l[i] - (o[i]-1)*w[i] )

for i1 in range(N):
    for i2 in range(i1+1, N):
        model.Add(x2[i1]<=x1[i2]).OnlyEnforceIf(xmn[i1][i2])
        model.Add(x2[i1]> x1[i2]).OnlyEnforceIf(xmn[i1][i2].Not())
        model.Add(y2[i1]<=y1[i2]).OnlyEnforceIf(ymn[i1][i2])
        model.Add(y2[i1]> y1[i2]).OnlyEnforceIf(ymn[i1][i2].Not())
        model.Add(x2[i2]<=x1[i1]).OnlyEnforceIf(xnm[i1][i2])
        model.Add(x2[i2]> x1[i1]).OnlyEnforceIf(xnm[i1][i2].Not())
        model.Add(y2[i2]<=y1[i1]).OnlyEnforceIf(ynm[i1][i2])
        model.Add(y2[i2]> y1[i1]).OnlyEnforceIf(ynm[i1][i2].Not())

        model.Add(p[i1]==p[i2]).OnlyEnforceIf(t[i1][i2])
        model.Add(p[i1]!=p[i2]).OnlyEnforceIf(t[i1][i2].Not())
        
        model.AddBoolOr([xmn[i1][i2], ymn[i1][i2], xnm[i1][i2], ynm[i1][i2]]).OnlyEnforceIf(t[i1][i2])

# obj = model.NewIntVar(0, sum_c, 'obj')
# model.Add(sum(u[j]*c[j] for j in range(K)) == obj)
model.Minimize(sum(u[j]*c[j] for j in range(K)))
start = time.time()
solver = cp_model.CpSolver()
status = solver.Solve(model)
duration = time.time() - start
if status == cp_model.OPTIMAL:
    print('Time = {} seconds'.format(duration))
    print('Obj = %i' % solver.ObjectiveValue())
    for i in range(N):
        for j in range(K):
            if(solver.Value(p_bool[i][j])):
                print('package {} at truck {}, orientation {}, bottom-left: ({}, {}), top-right: ({}, {})'.format(i, j, \
                    solver.Value(o[i]), solver.Value(x1[i]), solver.Value(y1[i]), solver.Value(x2[i]), solver.Value(y2[i])))
else:
    print(solver.StatusName(status))        
