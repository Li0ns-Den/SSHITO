import numpy as np
import pandas as pd

def readcoord(filepath):

    df = pd.read_csv(filepath)

    dat = df.to_numpy()
    x = dat[:,0]
    y = dat[:,1]

    return x, y

def readperf(filepath):

    df = pd.read_csv(filepath)

    dat = df.to_numpy()
    x = dat[:,0]
    AR = dat[:,1]
    M = dat[:,2]
    P = dat[:,3]
    T = dat[:,4]
    rho = dat[:,5]
    V = dat[:,6]

    return x, AR, M, P, T, rho, V


