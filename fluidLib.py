from pyfluids import Fluid, FluidsList, Input, Phases

liq = Fluid(FluidsList.Oxygen)

P_liq = 30e5
T_liq = 80

liq.update(Input.pressure(P_liq), Input.temperature(T_liq))

Cp = liq.specific_heat
rho = liq.density
mu = liq.dynamic_viscosity
k = liq.conductivity

liq = liq.dew_point_at_pressure(P_liq)
T_sat = liq.temperature

local_vars = dict(locals()) 
for var_name, var_value in local_vars.items():
    if not var_name.startswith('_'):  # Skip internal Python vars
        print(f"{var_name} = {var_value}")