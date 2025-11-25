from pyfluids import Fluid, FluidsList, Input, Phases
import numpy as np
def input():

    In = {

        'Tc'            : 'perf.csv', # or 'filename.csv' for importing contours
        'Tl0'           : 218,

        'hg'            : 'calculate', # or 'calculate'
        'Cpg'           : 5.9e3,
        'mug'           : 1.07e-4,
        'kg'            : 14.0e-1,
        # 'Cpg'           : 2.22e3,
        # 'mug'           : 1.07e-4,
        # 'kg'            : 3.75e-1,
        
        'hl'            : 'calculate', # or 'calculate'
        'pyfluids'      : True,
        'liqType'       : Fluid(FluidsList.nPropane),
        'P_liq'         : 6e6,
        'Cpl'           : 1.66e3,
        'm_dot_l'       : 1.1,
        'AR_surf'       : 1, # Account for increased surface area from grooves tubes etc.
        'adjust_AR_surf': True, #
        'A_cs'          : 1.5*1.2e-3,
        'adjust_Acs'    : False, # Or off to target area
        'mul'           : 2.652e-4,
        'roughness'     : 0.15e-3,
        'rhol'          : 1199,
        'kl'            : 0.168,
        'T_boil'        : np.nan,
        'dT_nucleate'   : np.nan,

        'tw'            : 2.5e-3,
        'kw'            : 280,

        'flowdir'       : 'AF', # FA (FWD-AFT) or AF (AFT-FWD)

        
        'l_c'           : 'contour.csv', # or 'filename.csv' for importing contours
        'D_c'           : .15, # or 'filename.csv' for importing contours
        'N_nodes'       : 200,

        'l_modifier'    :1e-3,
            
    }

    return In