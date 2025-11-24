import numpy as np

def findFluxTotal(Tc, Tl, hg, hl, tw, kw):

    q = (Tc-Tl)/((1/hg)+(tw/kw)+(1/hl))

    return q

def findTwg(q, Tc, hg):

    Twg = Tc - (q/hg)

    return Twg

def findTwl(Twg, q, tw, kw):
    
    Twl = Twg - (tw * q / kw)

    return Twl

def findhg(rho, v, D, Pr, kg, mu):

    hg = 0.026*(((rho*v)**0.8)/(D**0.2))*(Pr**0.4)*(kg / (mu**0.8))
    # hg = (rho*v)**0.8

    return hg

def findPr(Cp,mu,k):

    Pr = Cp*mu/k

    return Pr

def findhl(Cp, D, rho, v, mu, A, m_dot, kl):

    hl = 0.023*Cp*(m_dot/A)*(((D*v*rho)/(mu))**0.2)*((mu*Cp)/kl)**(-2/3)

    return hl

def finddT(q, m_dot, Cp, A):

    dT = (q*A) / (m_dot*Cp)
    
    return dT