from ortools.sat.python import cp_model
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

N, K, w, l, W, L, c = input('data/test-data-1.txt')
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

model = cp_model.CpModel()
# variables
x1 = [model.NewIntVar(0,max_W,'x1['+str(i)+']') for i in range(N)]
y1 = [model.NewIntVar(0,max_L,'y1['+str(i)+']') for i in range(N)]
o = [model.NewBoolVar('o['+str(i)+']') for i in range(N)]
p = [[model.NewIntVar(0, 1, 'p['+str(i)+','+str(j)+']') for j in range(K)] for i in range(N)]
# extra variables
x2 = [model.NewIntVar(0,max_W,'x2['+str(i)+']') for i in range(N)]
y2 = [model.NewIntVar(0,max_L,'y2['+str(i)+']') for i in range(N)]
t = [[model.NewBoolVar('t['+str(i1)+','+str(i2)+']') for i2 in range(N)] for i1 in range(N)]
p_bool = [[model.NewBoolVar('p_bool['+str(i)+','+str(j)+']') for j in range(K)] for i in range(N)]
p_n = [model.NewIntVar(0,K-1,'y2['+str(i)+']') for i in range(N)]
u = [model.NewIntVar(0, 1, 'u['+str(j)+']') for j in range(K)]
u_bool = [model.NewBoolVar('u_bool['+str(j)+']') for j in range(K)]

xmn = [[model.NewBoolVar('xmn['+str(i1)+','+str(i2)+']') for i2 in range(N)] for i1 in range(N)]
ymn = [[model.NewBoolVar('ymn['+str(i1)+','+str(i2)+']') for i2 in range(N)] for i1 in range(N)]
xnm = [[model.NewBoolVar('xnm['+str(i1)+','+str(i2)+']') for i2 in range(N)] for i1 in range(N)]
ynm = [[model.NewBoolVar('ynm['+str(i1)+','+str(i2)+']') for i2 in range(N)] for i1 in range(N)]

for i1 in range(N):
    for i2 in range(N):
        model.Add(x2[i1]<=x1[i2]).OnlyEnforceIf(xmn[i1][i2])
        model.Add(x2[i1]> x1[i2]).OnlyEnforceIf(xmn[i1][i2].Not())
        model.Add(y2[i1]<=y1[i2]).OnlyEnforceIf(ymn[i1][i2])
        model.Add(y2[i1]> y1[i2]).OnlyEnforceIf(ymn[i1][i2].Not())
        model.Add(x2[i2]<=x1[i1]).OnlyEnforceIf(xnm[i1][i2])
        model.Add(x2[i2]> x1[i1]).OnlyEnforceIf(xnm[i1][i2].Not())
        model.Add(y2[i2]<=y1[i1]).OnlyEnforceIf(ynm[i1][i2])
        model.Add(y2[i2]> y1[i1]).OnlyEnforceIf(ynm[i1][i2].Not())

for j in range(K):
    model.Add(u[j]==1).OnlyEnforceIf(u_bool[j])
    model.Add(u[j]==0).OnlyEnforceIf(u_bool[j].Not())
    model.AddBoolOr([p_bool[i][j] for i in range(N)]).OnlyEnforceIf(u_bool[j])
    model.AddBoolAnd([p_bool[i][j].Not() for i in range(N)]).OnlyEnforceIf(u_bool[j].Not())

for i in range(N):
    for j in range(K):
        model.Add(p[i][j]==1).OnlyEnforceIf(p_bool[i][j])
        model.Add(p[i][j]==0).OnlyEnforceIf(p_bool[i][j].Not())
        model.Add(p_n[i]==j).OnlyEnforceIf(p_bool[i][j])
        model.Add(p_n[i]!=j).OnlyEnforceIf(p_bool[i][j].Not())
        # constraint: don't put package out of the truck
        model.Add(x2[i]<=W[j]).OnlyEnforceIf(p_bool[i][j])
        model.Add(y2[i]<=L[j]).OnlyEnforceIf(p_bool[i][j])

for i in range(N):
    model.Add( (x2[i]-x1[i])==l[i] ).OnlyEnforceIf(o[i])
    model.Add( (y2[i]-y1[i])==w[i] ).OnlyEnforceIf(o[i])
    model.Add( (x2[i]-x1[i])==w[i] ).OnlyEnforceIf(o[i].Not())
    model.Add( (y2[i]-y1[i])==l[i] ).OnlyEnforceIf(o[i].Not())

for i in range(N):
    model.Add(sum(p[i][j] for j in range(K))==1)

for i1 in range(N):
    for i2 in range(N):
        # model.AddBoolAnd([p_bool[i1][j], p_bool[i2][j]]).OnlyEnforceIf(t[i1][i2])
        # model.AddBoolOr([p_bool[i1][j].Not(), p_bool[i2][j].Not()]).OnlyEnforceIf(t[i1][i2].Not())
        if i1 != i2:
            model.Add(p_n[i1]==p_n[i2]).OnlyEnforceIf(t[i1][i2])
            model.Add(p_n[i1]!=p_n[i2]).OnlyEnforceIf(t[i1][i2].Not())
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
                print('package {} at truck {}, bottom-left: ({}, {}), top-right: ({}, {})'.format(i, j, \
                    solver.Value(x1[i]), solver.Value(y1[i]), solver.Value(x2[i]), solver.Value(y2[i])))
else:
    print(solver.StatusName(status))        
