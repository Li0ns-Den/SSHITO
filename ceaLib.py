from rocketcea.cea_obj_w_units import CEA_Obj, CEA_Obj_default

Ox = 'LOX'
Fuel = 'Propane'

CEAdata = CEA_Obj(oxName = Ox, fuelName = Fuel, pressure_units='Pa', temperature_units='K')
CEAdata_default = CEA_Obj_default(oxName = Ox, fuelName = Fuel)
CEAout = CEAdata_default.get_full_cea_output( Pc= 40, MR=1, eps=20, short_output=0, pc_units = 'bar',output='siunits')
# s = CEAdata.get_full_cea_output( Pc=40e5, MR=2.65, eps=20, short_output=0)

print(CEAout)