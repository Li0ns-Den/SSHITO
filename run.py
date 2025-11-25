import numpy as np
from pyfluids import Fluid, FluidsList, Input, Phases
import matplotlib.pyplot as plt
import matplotlib as mpl
import htFunctions as hf
import arrayEditor as ae
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

if In['pyfluids'] == True:
    liqObj = In['liqType']

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
v_l          = np.zeros(len(l))
P_l         = np.zeros(len(l))

dT          = 0


Tl[0]       = Tl0
P_l[0]       = In['P_liq']

if In['adjust_Acs'] == True or In['adjust_AR_surf'] == True:

    fig, ax0 = plt.subplots()
    ax0.plot(l,D/2, linestyle = '-', color = 'tab:orange', label = 'Gas Side Wall')
    ax0.set_xlabel('Axial Position, m')
    ax0.set_ylabel('Radial Position, m')
    ax0.set_ylim([0, (D.max() + D.max()*0.1) / 2])
    ax0.set_aspect('equal')
    ax0.grid()
    ax0.minorticks_on()
    ax0.grid(which='major', linestyle='-', linewidth='0.5')
    ax0.grid(which='minor', linestyle=':', linewidth='0.5')
    ax0.legend()

if In['adjust_Acs'] == True:

    _, A_cs = ae.edit(In['A_cs'],0,l.max(),15,N_n)
    if In['flowdir'] == 'AF':
        A_cs = np.flip(A_cs)
else:
    A_cs = np.zeros(len(l))
    A_cs[:] = In['A_cs']

if In['adjust_AR_surf'] == True:
        
    _, AR_surf = ae.edit(In['AR_surf'],0,l.max(),15,N_n)
    if In['flowdir'] == 'AF':
        AR_surf = np.flip(AR_surf)    
else:
    AR_surf = np.zeros(len(l))
    AR_surf[:] = In['AR_surf']         

for i, val in enumerate(l):

    if i == 0:
        Tl[i] = Tl[i]
        P_l[i] = P_l[i]
    else:
        Tl[i] = Tl[i-1] + dT
        P_l[i] = P_l[i-1] + dP

    if hg == 'calculate':

        Pr = hf.findPr(In['Cpg'],In['mug'],In['kg'])
        hg_calc = hf.findhg(rho[i],V[i],D[i],Pr,In['kg'], In['mug'])
        # print(hg_calc)
    else:
        hg_calc = hg

    if hl == 'calculate':

        if In['pyfluids'] == True:
            liqObj.update(Input.pressure(P_l[i]), Input.temperature(Tl[i]))
            Cpl = liqObj.specific_heat
            rhol = liqObj.density
            mul = liqObj.dynamic_viscosity
            kl = liqObj.conductivity
        else:
            Cpl = In['Cpl']
            rhol = In['rhol']
            mul = In['mul']
            kl = In['kl']

        v_l[i] = In['m_dot_l']/(rhol*A_cs[i])

        R_hydro = A_cs[i] / (np.pi * (AR_surf[i]*D[i] + (tw*2)))
        D_eq = 4*R_hydro
        hl_calc = hf.findhl(Cpl, D_eq, rhol, v_l[i], mul, A_cs[i], In['m_dot_l'], kl)
        # print(hl_calc)
    else:
        hl_calc = hl

    q[i] = hf.findFluxTotal(T[i], Tl[i], hg_calc, hl_calc, tw, kw, AR_surf[i])

    Twg[i] = hf.findTwg(q[i], T[i], hg_calc)

    Twl[i] = hf.findTwl(Twg[i], q[i], tw, kw)
    try:
        A = np.pi*D[i]*dl
    except:
        A = np.pi*D*dl

    dT = hf.finddT(q[i], m_dot_l, Cpl, A)
 
    C_fric = hf.FricCoeff(v_l[i],D_eq,mul,rhol,In['roughness'])

    dP = hf.finddP(C_fric,dl,D_eq,rhol,v_l[i])

    # print(v_l[i])

    dQ[i] = q[i]*A

    D_wl[i] = D[i] + 2*tw
    t_chn = (np.sqrt(((4*A_cs[i])/np.pi)+D_wl[i]**2)-D_wl[i])/2
    D_chn[i] = D_wl[i] + t_chn

Q_total = sum(dQ)

# local_vars = dict(locals()) 
# for var_name, var_value in local_vars.items():
#     if not var_name.startswith('_'):  # Skip internal Python vars
#         print(f"{var_name} = {var_value}")

fig, ax = plt.subplots(3,sharex=True)

titleText = f'Wall temperatures @ $T_{{c,max}}$ = {T.max().round(0)}$K$ along axial positions'

ax[1].set_title(titleText, fontsize = 15)
ax[1].plot(l,Tl, linestyle = '-', color = 'k', label = '$T_l$, Bulk Liquid')
ax[1].plot(l,Twl, linestyle = '--', color = 'k', label = '$T_{wl}$, Wall Liquid Side')
ax[1].plot(l,Twg, linestyle = '-.', color = 'k',  label = '$T_{wg}$, Wall Gas Side')
ax[1].axhline(y = In['T_boil'], color = 'tab:red', linestyle = '-', label = '$T_{{vap}}$, Liquid Vapor/Boiling Temperature')
ax[1].axhline(y = In['T_boil'] + In['dT_nucleate'], color = 'tab:red', linestyle = '--', label = '$T_{{nucleate}}$ Wall Liquid Side Threshold' )

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

ax[2].set_title('Channel Velocity + Pressures', fontsize = 15)
ln1 = ax[2].plot(l,P_l/1e5, linestyle = '-', color = 'k', label = '$P_l$, Coolant Pressure')
ax2 = ax[2].twinx()
ln2 = ax2.plot(l,v_l, linestyle = '--', color = 'k', label = '$P_l$, Coolant Velocity')
ax[2].set_xlabel('Axial Position, m')
ax[2].set_ylabel('Pressure, $bar$')
ax2.set_ylabel('Velocity, $ms^{-1}$')
# ax[2].set_ylim([P_l.min()*0.9/1e5, P_l.max()*1.1/1e5])
# ax2.set_ylim([v_l.min()*0.9, v_l.max()*1.1])
ax[2].grid()
ax[2].minorticks_on()
ax[2].grid(which='major', linestyle='-', linewidth='0.5')
ax[2].grid(which='minor', linestyle=':', linewidth='0.5')
lns = ln1+ln2
labs = [l.get_label() for l in lns]
ax[2].legend(lns, labs, loc=0)

plt.show()

 