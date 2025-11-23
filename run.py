import numpy as np
import matplotlib.pyplot as plt
import htFunctions as hf
import inputs

In = inputs.input()

Tc          = In['Tc']
Tl0         = In['Tl0']
hg          = In['hg']
hl          = In['hl']
tw          = In['tw']
kw          = In['kw']
l_c         = In['l_c']
D_c         = In['D_c']
m_dot_l     = In['m_dot_l']
N_n         = In['N_nodes']
Cpl         = In['Cpl']

l           = np.linspace(0,l_c,N_n)
dl          = l[1]
Tl          = np.zeros(len(l))
q           = np.zeros(len(l))
Twg         = np.zeros(len(l))
Twl         = np.zeros(len(l))
dQ          = np.zeros(len(l))
dT          = 0


Tl[0]       = Tl0

for i, val in enumerate(l):

    if i == 0:
        Tl[i] = Tl[i]
    else:
        Tl[i] = Tl[i-1] + dT

    q[i] = hf.findFluxTotal(Tc, Tl[i], hg, hl, tw, kw)

    Twg[i] = hf.findTwg(q[i], Tc, hg)

    Twl[i] = hf.findTwl(Twg[i], q[i], tw, kw)

    A = np.pi*D_c*dl

    dT = hf.finddT(q[i], m_dot_l, Cpl, A)

    dQ[i] = q[i]*A

Q_total = sum(dQ)

local_vars = dict(locals()) 
for var_name, var_value in local_vars.items():
    if not var_name.startswith('_'):  # Skip internal Python vars
        print(f"{var_name} = {var_value}")

fig = plt.figure()

plt.plot(l,Tl)
plt.plot(l,Twl)
plt.plot(l,Twg)

plt.show()

 