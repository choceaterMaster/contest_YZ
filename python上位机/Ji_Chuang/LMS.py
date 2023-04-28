import numpy as np

def aver(x,N=2):
    L=len(x)
    d=np.zeros(L)
    sum=np.zeros(3)
    for n in range(L):
        try:
            if(n>=2):
                sum=x[n-N:n]
                av=np.average(sum)
                d[n]=av
            else:
                d[n]=x[n]
        except:
            print("sum=",sum)
    return d
def lms(x, d, N = 4, mu = 0.02): #x:输入 d:期望输出？ N:与迭代次数有关 mu:步长
    L = min(len(x),len(d))
    h = np.zeros(N)
    e = np.zeros(L-N)
    for n in range(L-N):
        x_n = x[n:n+N][::-1]
        d_n = d[n]
        y_n = np.dot(h, x_n.T)
        e_n = d_n - y_n
        h = h + mu * e_n * x_n
        e[n] = e_n
    return e

