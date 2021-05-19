input_file = './container_input.txt'

with open(input_file) as f:
    [n, k] = [int(x) for x in f.readline().split()]

    w, l = {}, {}
    w[0], w[1] = {}, {}
    l[0], l[1] = {}, {}
    for ii in range(n):
        [i,j] = [int(x) for x in f.readline().split()]
        w[0][ii] = i
        l[0][ii] = j
        w[1][ii] = j
        l[1][ii] = i
    

    W,L,c = [], [], []
    for _ in range(k):
        [W_,L_,c_] = [int(x) for x in f.readline().split()]
        W.append(W_)
        L.append(L_)
        c.append(c_)

x1 = {}
y1 = {}
# p[i] = j gói hàng i đặt vào xe j
p = {}
o = {}
# u[j]: xe j được sủ dụng u[j] lần
u = {}
for i in range(k):
    u[i] = 0

x1Best, y1Best, pBest, oBest = {}, {}, {}, {}
cost = 0
bestCost = float('inf')

# gói hàng i, xe tải j, toạ độ (x1i, y1i), hướng oi
def canPut(i, j, x1i, y1i, oi):
    # kiểm tra xe gói hàng i có cho vào xe j được hay không
    x2i = x1i + w[oi][i]
    y2i = y1i + l[oi][i]
    if x2i > W[j] or y2i > L[j]:
        return False

    # kiểm tra xem 2 thùng có chồng lên nhau hay không
    for i2 in range(i):
        if p[i2] == j:
            x2i2 = x1[i2] + w[o[i2]][i2]
            y2i2 = y1[i2] + l[o[i2]][i2]
            if not (x2i2 <= x1i or x2i <= x1[i2] or y2i2 <= y1i or y2i <= y1[i2]):
                return False
    
    return True

# để gói hàng i vào xe j
def put(i, j, x1i, y1i, oi):
    global p, x1, y1, o, u, cost
    p[i] = j
    x1[i] = x1i
    y1[i] = y1i
    o[i] = oi
    if u[j] == 0:
        cost += c[j]
    u[j] += 1

def pop(j):
    global u, cost
    if u[j] == 1:
        cost -= c[j]
    u[j] -= 1

def updateBest():
    global bestCost, cost, x1Best, y1Best, pBest, oBest
    bestCost = cost
    for i in range(n):
        x1Best[i] = x1[i]
        y1Best[i] = y1[i]
        pBest[i] = p[i]
        oBest[i] = o[i]
    print(bestCost)

iter = 0
def Try(i):
    global cost, iter
    iter += 1 
    for j in range(k):
        for x1i in range(W[j]):
            for y1i in range(L[j]):
                for oi in range(2):
                    if canPut(i, j, x1i, y1i, oi):
                        put(i,j,x1i,y1i,oi)
                        if i < n-1:
                            if cost < bestCost:
                                Try(i+1)
                        else:
                            if cost < bestCost:
                                updateBest()
                        pop(j)

Try(0)




            
        




