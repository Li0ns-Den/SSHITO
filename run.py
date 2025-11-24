import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import htFunctions as hf
import readcsv as rcsv
import inputs

try:
    mpl.rc('text', usetex=True)
    fig, ax = plt.subplots(1, 1, figsize=(1, 1))
    fig.canvas.draw()
    mpl.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})  # This is where it would fail if LaTeX doesn't work
    plt.close(fig)
except:
    plt.close(fig)
    mpl.rc('text', usetex=False)
    print('Error: LaTeX not found')

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


if isinstance(l_c, str) or isinstance(D_c, str):
    if l_c.endswith('.csv') or D_c.endswith('.csv'):

        try:
            l_dat, r_dat = rcsv.readcoord(l_c)
        except:
            l_dat, r_dat = rcsv.readcoord(D_c)

        l           = np.linspace(0,l_dat.max(),N_n)
        D           = np.interp(l,l_dat,r_dat) * 2
        l = l * In['l_modifier']
        D = D * In['l_modifier']

    else:
        print('error, unsupported file path for importing contour, exiting')
        exit()

    if In['flowdir'] == 'AF':
        l = np.flip(l)
        D = np.flip(D)
else:
    l           = np.linspace(0,l_c,N_n)
    D        = np.zeros(len(l))
    D[:]           = D_c

if isinstance(Tc, str):
    if Tc.endswith('.csv'):

        l_dat , AR_dat, M_dat, P_dat, T_dat, rho_dat, V_dat  = rcsv.readperf(Tc)
        l = np.linspace(0,l_dat.max(),N_n)
        AR = np.interp(l,l_dat,AR_dat)
        M = np.interp(l,l_dat,M_dat)
        P = np.interp(l,l_dat,P_dat)
        T = np.interp(l,l_dat,T_dat)
        rho = np.interp(l,l_dat,rho_dat)
        V = np.interp(l,l_dat,V_dat)
        l = l * In['l_modifier']

    else:
        print('error, unsupported file path for importing contour, exiting')
        exit()

    if In['flowdir'] == 'AF':
        l = np.flip(l)
        AR = np.flip(AR)
        M = np.flip(M)
        P = np.flip(P)
        T = np.flip(T)
        rho = np.flip(rho)
        V = np.flip(V)
else:
    T        = np.zeros(len(l))
    T[:] = Tc

dl          = abs(l[1]-l[0])
Tl          = np.zeros(len(l))
q           = np.zeros(len(l))
Twg         = np.zeros(len(l))
Twl         = np.zeros(len(l))
dQ          = np.zeros(len(l))
D_wl        = np.zeros(len(l))
D_chn      = np.zeros(len(l))

dT          = 0


Tl[0]       = Tl0

for i, val in enumerate(l):

    if i == 0:
        Tl[i] = Tl[i]
    else:
        Tl[i] = Tl[i-1] + dT

    if hg == 'calculate':

        Pr = hf.findPr(In['Cpg'],In['mug'],In['kg'])
        hg_calc = hf.findhg(rho[i],V[i],D[i],Pr,In['kg'], In['mug'])
        # print(hg_calc)
    else:
        hg_calc = hg

    if hl == 'calculate':
        v_l = In['m_dot_l']/(In['rhol']*In['A_CS'])
        R_hydro = In['C_wetToNominal']*In['A_CS'] / (np.pi * (D[i] + (tw*2)))
        D_eq = 4*R_hydro
        hl_calc = hf.findhl(In['Cpl'], D_eq, In['rhol'], v_l, In['mul'], In['A_CS'], In['m_dot_l'], In['kl'])
        print(hl_calc)
    else:
        hl_calc = hl

    q[i] = hf.findFluxTotal(T[i], Tl[i], hg_calc, hl_calc, tw, kw)

    Twg[i] = hf.findTwg(q[i], T[i], hg_calc)

    Twl[i] = hf.findTwl(Twg[i], q[i], tw, kw)
    try:
        A = np.pi*D[i]*dl
    except:
        A = np.pi*D*dl

    dT = hf.finddT(q[i], m_dot_l, Cpl, A)

    dQ[i] = q[i]*A

    D_wl[i] = D[i] + 2*tw
    t_chn = (np.sqrt(((4*In['A_CS'])/np.pi)+D_wl[i]**2)-D_wl[i])/2
    D_chn[i] = D_wl[i] + t_chn

Q_total = sum(dQ)

# local_vars = dict(locals()) 
# for var_name, var_value in local_vars.items():
#     if not var_name.startswith('_'):  # Skip internal Python vars
#         print(f"{var_name} = {var_value}")

fig, ax = plt.subplots(2,sharex=True)

titleText = f'Wall temperatures @ $T_{{c,max}}$ = {T.max().round(0)}$K$ along axial positions'

ax[1].set_title(titleText, fontsize = 15)
ax[1].plot(l,Tl, linestyle = '-', color = 'k', label = '$T_l$, Bulk Liquid')
ax[1].plot(l,Twl, linestyle = '--', color = 'k', label = '$T_{wl}$, Wall Liquid Side')
ax[1].plot(l,Twg, linestyle = '-.', color = 'k',  label = '$T_{wg}$, Wall Gas Side')

ax[1].set_xlabel('Axial Position, m')
ax[1].set_ylabel('Temperature, K')
ax[1].grid()
ax[1].minorticks_on()
ax[1].grid(which='major', linestyle='-', linewidth='0.5')
ax[1].grid(which='minor', linestyle=':', linewidth='0.5')
ax[1].legend()

if In['flowdir'] == 'AF':
    ax[0].set_title('Coolant Flow Direction: FWD $<$--------- AFT', fontsize = 15)
else:
    ax[0].set_title('Coolant Flow Direction: FWD ---------$>$ AFT', fontsize = 15)

ax[0].plot(l,D_chn/2, linestyle = '-', color = 'k', label = 'Outer Channal Contour')
ax[0].plot(l,D_wl/2, linestyle = '--', color = 'k', label = 'Inner Channel Contour')
ax[0].plot(l,D/2, linestyle = '-', color = 'tab:orange', label = 'Gas Side Wall')
ax[0].set_xlabel('Axial Position, m')
ax[0].set_ylabel('Radial Position, m')
ax[0].set_ylim([0, (D.max() + D.max()*0.1) / 2])
ax[0].set_aspect('equal')
ax[0].grid()
ax[0].minorticks_on()
ax[0].grid(which='major', linestyle='-', linewidth='0.5')
ax[0].grid(which='minor', linestyle=':', linewidth='0.5')
ax[0].legend()


plt.show()

 