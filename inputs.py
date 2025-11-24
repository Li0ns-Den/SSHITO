def input():

    In = {

        'Tc'            : 'perf.csv', # or 'filename.csv' for importing contours
        'Tl0'           : 80,

        'hg'            : 'calculate', # or 'calculate'
        # 'Cpg'           : 5.9e3,
        # 'mug'           : 1.07e-4,
        # 'kg'            : 14.0e-1,
        'Cpg'           : 2.22e3,
        'mug'           : 1.07e-4,
        'kg'            : 3.75e-1,
        
        'hl'            : 'calculate', # or 'calculate'
        'Cpl'           : 1.66e3,
        'm_dot_l'       : 2.97,
        'C_wetToNominal': 1, # Account for increased surface area from grooves tubes etc.
        'A_CS'          : 10*1.2e-3,
        'mul'           : 2.652e-4,
        'rhol'          : 1199,
        'kl'            : 0.168,
        'T_boil'        : 141.69,
        'dT_nucleate'   : 10,

        'tw'            : 5e-3,
        'kw'            : 200,

        'flowdir'       : 'AF', # FA (FWD-AFT) or AF (AFT-FWD)

        
        'l_c'           : 'contour.csv', # or 'filename.csv' for importing contours
        'D_c'           : .15, # or 'filename.csv' for importing contours
        'N_nodes'       : 200,

        'l_modifier'    :1e-3,
            
    }

    return In