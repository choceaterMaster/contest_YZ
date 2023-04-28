import numpy as np
#一维卡尔曼滤波
def kalman_filter(data,Q=1,R=1):
    N=len(data)
    z=data #观测值
    xt=np.zeros(N) #估计值
    xt_=np.zeros(N)
    pt_=np.ones(N) + 0.35 # 开始不可取0
    pt=np.ones(N)+ 0.35
    out=np.ones(N)
    F=1
    for n in range(N):
        if(n>0):
            xt_[n]=F * xt[n-1]
        else:
            xt_[n]=0
        pt_[n]=np.cov(xt) #自身的协方差
        _FenMu=(pt[n-1]+Q+R)
        kt=(pt[n-1]+Q) / _FenMu
        xt[n]=xt_[n] + kt * (z[n] - xt_[n])
        # pt[n]=np.dot((I - kt),pt_[n])
        pt[n]=(1-kt)*pt_[n]
        out[n]=xt[n]
    return out,pt,kt