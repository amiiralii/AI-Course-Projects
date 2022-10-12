import pandas as pd
import random
import time

CHROMLEN = 9
CHROMNUM = 21
CHROMNUM2 = 9

def isCorrect(sample, solution):
    input1 = solution[0]
    j = 0
    for i in range(len(sample)):
        if sample[i]==0:
            j = int( (input1 + solution[i+1]) == 2 )
        if sample[i]==1:
            j = int( (input1 + solution[i+1]) != 2 )
        if sample[i]==2:
            j = int( (input1 + solution[i+1]) != 0 )
        if sample[i]==3:
            j = int( (input1 + solution[i+1]) == 0 )
        if sample[i]==4:
            j = (input1 + solution[i+1]) % 2
        if sample[i]==5:
            j = (input1 + solution[i+1] + 1) % 2
        ##print('operation =', sample[i],'input =', input1, 'input =', solution[i+1], 'output =', j)
        input1 = j
    if j==solution[-1]:
        return 1
    else:
        return 0
def fitness(solution, df):
    s=0
    for i in df:
       s += isCorrect(solution, i)
    return s
def mutate(l):
    p = random.randrange(0, CHROMLEN)
    l[p] = random.randrange(0, 6)
    return l
def mutate2(l):
    p = random.randrange(0, CHROMLEN)
    l[p] = random.randrange(0, 6)
    p = random.randrange(0, CHROMLEN)
    l[p] = random.randrange(0, 6)
    return l
def onePointmix(l1, l2):
    point = random.randrange(0, CHROMLEN)
    out = []
    for i in range(len(l1)):
        if i <= point:
            out.append(l1[i])
        else:
            out.append(l2[i])
    return out
def twoPointmix(l1, l2):
    point = random.randrange(0, CHROMLEN)
    point2 = random.randrange(0, CHROMLEN)
    if point>point2:
        temp = point
        point = point2
        point2 = temp
    out = []
    for i in range(len(l1)):
        if i <= point:
            out.append(l1[i])
        elif i < point2:
            out.append(l2[i])
        else:
            out.append(l1[i])
    return out
def generateNextGen(current, val):
    newgen = []
    for i in range(0, 3):
        newgen.append(current[val[i]])
    for i in range(7, 9):
        k = mutate(current[val[i]])
        newgen.append(k)
    for i in range(9, 17):
        newgen.append(mutate(onePointmix(current[val[i-9]], current[val[i-8]])))
        newgen.append(mutate(onePointmix(current[val[i - 8]], current[val[i - 9]])))
    return newgen
def generateNextGen2(current, val):
    newgen = []
    for i in range(0, 3):
        newgen.append(current[val[i]])
    for i in range(7, 9):
        k = mutate(current[val[i]])
        newgen.append(k)
    for i in range(9, 17):
        newgen.append(mutate(twoPointmix(current[val[i-9]], current[val[i-8]])))
        newgen.append(mutate(twoPointmix(current[val[i - 8]], current[val[i - 9]])))
    return newgen
def generateNextGen3(current, val):
    newgen = []
    for i in range(0, 3):
        newgen.append(current[val[i]])
    for i in range(7, 9):
        k = mutate2(current[val[i]])
        newgen.append(k)
    for i in range(9, 17):
        newgen.append(mutate2(onePointmix(current[val[i-9]], current[val[i-8]])))
        newgen.append(mutate2(onePointmix(current[val[i - 8]], current[val[i - 9]])))
    return newgen
def generateNextGen4(current, val):
    newgen = []
    for i in range(0, 3):
        newgen.append(current[val[i]])
    for i in range(3, 6):
        k = mutate(current[val[i]])
        newgen.append(k)

    newgen.append(mutate(onePointmix(current[val[1]], current[val[0]])))
    newgen.append(mutate(onePointmix(current[val[0]], current[val[2]])))
    newgen.append(mutate(onePointmix(current[val[1]], current[val[2]])))
    return newgen
def generateNextGen5(current, val):
    newgen = []
    for i in range(0, 3):
        newgen.append(current[val[i]])
    for i in range(7, 9):
        k = mutate2(current[val[i]])
        newgen.append(k)
    for i in range(9, 17):
        newgen.append(mutate2(twoPointmix(current[val[i-9]], current[val[i-8]])))
        newgen.append(mutate2(twoPointmix(current[val[i - 8]], current[val[i - 9]])))
    return newgen
def printSol(l):
    for i in l:
        if i==0:
            print('And', end=' ,')
        if i==1:
            print('Nand', end=' ,')
        if i==2:
            print('Or', end=' ,')
        if i==3:
            print('Nor', end=' ,')
        if i==4:
            print('Xor', end=' ,')
        if i==5:
            print('Xnor', end=' ,')
df = pd.read_csv('truth_table.csv')
df.replace(to_replace =True, value =1, inplace=True)
df.replace(to_replace =False, value =0, inplace=True)
template = [df.columns.values.tolist()] + df.values.tolist()
template = template[1:]


print('Result for 21 chromosomes per each generation Using onepoint crossover.')
print()
tt = 0
ss = 0
## First try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('First try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
## Second try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('Second try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
## Third try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('Third try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
print('Average time duration for this algorithm:', tt/3)
print('Average steps for this algorithm:', ss/3)
print()


print('Result for 21 chromosomes per each generation Using twopoint crossover.')
print()
tt = 0
ss = 0
## First try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('First try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen2(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
## Second try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('Second try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen2(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
## Third try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('Third try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen2(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
print('Average time duration for this algorithm:', tt/3)
print('Average steps for this algorithm:', ss/3)
print()


print('Result for 21 chromosomes per each generation Using onepoint crossover and mutate1.')
print()
tt = 0
ss = 0
## First try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('First try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
## Second try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('Second try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
## Third try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('Third try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
print('Average time duration for this algorithm:', tt/3)
print('Average steps for this algorithm:', ss/3)
print()


print('Result for 21 chromosomes per each generation Using onepoint crossover and mutate2.')
print()
tt = 0
ss = 0
## First try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('First try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen3(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
## Second try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('Second try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen3(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
## Third try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('Third try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen3(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
print('Average time duration for this algorithm:', tt/3)
print('Average steps for this algorithm:', ss/3)
print()


print('Result for 9 chromosomes per each generation Using onepoint crossover and mutate1.')
print()
tt = 0
ss = 0
## First try
gen = []
for i in range(CHROMNUM2):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM2):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('First try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM2):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen4(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
## Second try
gen = []
for i in range(CHROMNUM2):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM2):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('Second try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM2):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen4(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
## Third try
gen = []
for i in range(CHROMNUM2):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM2):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('Third try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM2):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen4(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
print('Average time duration for this algorithm:', tt/3)
print('Average steps for this algorithm:', ss/3)
print()



print('Result for 21 chromosomes per each generation Using onepoint crossover and mutate1.')
print()
tt = 0
ss = 0
## First try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('First try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
## Second try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('Second try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
## Third try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('Third try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
print('Average time duration for this algorithm:', tt/3)
print('Average steps for this algorithm:', ss/3)
print()


print('Result for 21 chromosomes per each generation Using onepoint crossover and mutate1.')
print()
tt = 0
ss = 0
## First try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('First try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen5(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
## Second try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('Second try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen5(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
## Third try
gen = []
for i in range(CHROMNUM):
    gen.append([random.randrange(0, 5, 1) for i in range(CHROMLEN)])
t1 = time.time()
step = 0
while True:
    f = []
    g = []
    for i in range(CHROMNUM):
        f.append(fitness(gen[i], template))
    k = max(f)
    maxIndex = f.index(k)
    if k==1024:
        print('Third try output :')
        print('One possible answer for gates is: ')
        printSol(gen[maxIndex])
        break
    for i in range(CHROMNUM):
        k = max(f)
        maxIndex = f.index(k)
        g.append(maxIndex)
        f[maxIndex] = 0
    gen = generateNextGen5(gen, g)
    step += 1
t2 = time.time()
tt += (((t2-t1)*100) // 1) / 100
ss += step
print(' Duration is', (((t2-t1)*100) // 1) / 100, 'seconds.')
print('Solved in', step, 'th generation.')
print()
print('Average time duration for this algorithm:', tt/3)
print('Average steps for this algorithm:', ss/3)
print()
