h= 58
w= 180

jstart = 1
jend = -1
jd = float(jend - jstart)/h

istart = -2
iend = 1
id = float(iend - istart)/w

def c_multiply(x, y):
    '''Complex multiply'''
    a, b = x
    c, d = y
    return (a*c-b*d, b*c+a*d)

def c_plus(x, y):
    '''Complex add'''
    a, b = x
    c, d = y
    return (a+c, b+d)

def mandel1(x, c):
    return c_plus(c_multiply(x,x), c)

def mandel2(x):
    a, b = x
    count = 0
    limit = 1000
    while abs(a) < 2 and abs(b) < 2 and count < limit:
        a, b = mandel1((a,b), x)
        count += 1
    if count < limit:
        return ' '
    return 'x'

for j in range(h):
    j1 = jstart + jd*j
    for i in range(w):
        i1 = istart + id*i
        #print((i1,j1))
        print(mandel2((i1,j1)), end='')
    print('')
