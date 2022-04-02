import png
import math

from joblib import Parallel, delayed
import multiprocessing
     

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

def mandel3(x):
    """ mandel2 but return color """
    a, b = x
    count = 0
    limit = 2000
    while abs(a) < 2 and abs(b) < 2 and count < limit:
        a, b = mandel1((a,b), x)
        count += 1

    brightness = float(count) / limit
    colorsum = brightness*255*3
    if colorsum >= 255:
        colorsum -= 255
        r = 255
    else:
        r = colorsum
        colorsum = 0
    if colorsum >= 255:
        colorsum -= 255
        g = 255
    else:
        g = colorsum
        colorsum = 0
    if colorsum >= 255:
        colorsum -= 255
        b = 255
    else:
        b = colorsum
        colorsum = 0
    
    return (int(b),int(g),int(r))

def ascii_draw(istart, iend, jstart, jend):
    h = 58
    w = 180
    jd = float(jend - jstart)/h
    id = float(iend - istart)/w

    for j in range(h):
        j1 = jstart + jd*j
        for i in range(w):
            i1 = istart + id*i
            #print((i1,j1))
            print(mandel2((i1,j1)), end='')
        print('')

def png_draw(istart, iend, jstart, jend):
    w=1920*2#1920
    h=1080*2#1080
    jd = float(jend - jstart)/h
    id = float(iend - istart)/w


    num_cores = multiprocessing.cpu_count()
    p = []
    for j in range(h):
        if j % 100 == 0:
            print(f"Processing status: {j/h}")
        j1 = jstart + jd*j
        l= ()
        results = Parallel(n_jobs=num_cores)(delayed(mandel3)((istart + id*i,j1)) for i in range(w))
        for i in range(w):
            i1 = istart + id*i
            #print((i1,j1))
            l = l + results[i]
        p.append(l)

    f = open('swatch2.png', 'wb')
    w = png.Writer(w, h, greyscale=False)
    w.write(f, p)
    f.close()


if __name__ == "__main__":
    midpoint = (-0.745, 0.1)
    #midpoint = (-math.e/7, -math.e/20)
    delta = .0005
    jstart = midpoint[1] + delta
    jend = midpoint[1] - delta

    istart = midpoint[0] - delta
    iend = midpoint[0] + delta

    #ascii_draw(istart, iend, jstart, jend)
    png_draw(istart, iend, jstart, jend)