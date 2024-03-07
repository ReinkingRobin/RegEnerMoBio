import sqlite3
import pandas as pd
from BiogasPlant import BiogasPlant

# define a connection to a database; if you reference a database which does not exists a new one will be created
conn = sqlite3.connect('ReferenceBiogasPlants.db')

# in the next step a cursor, which is able to interact with the database, need to be created
# the cursor allows us to create and modify tables in our database
c = conn.cursor()


# only execute once! -> which is the reason why we use CREATE TABLE IF NOT EXISTS
# and not CREATE TABLE
# c.execute("""CREATE TABLE IF NOT EXISTS BiogasPlants (
#             number integer,
#             feedstock integer,
#             bg_yield integer,
#             mth_yield integer,
#             dry_sub_cont real,
#             chpp_energy_supply integer,
#             ghg_avoidance real,
#             substrate_costs integer,
#             personnel_costs integer,
#             depreciation integer,
#             maintenance_costs integer,
#             electricity_demand integer,
#             heating_demand integer,
#             further_costs integer,
#             equity_ratio real,
#             debt_ratio real
#             )""")

# function for adding new biogas plant into database
def insert_biogas_plant(bp):
    with conn:
        c.execute("""INSERT INTO BiogasPlants VALUES (
                          :number,
                          :feedstock,
                          :bg_yield,
                          :mth_yield,
                          :dry_sub_cont,
                          :chpp_energy_supply,
                          :ghg_avoidance,
                          :substrate_costs,
                          :personnel_costs,
                          :depreciation,
                          :maintenance_costs,
                          :electricity_demand,
                          :heating_demand,
                          :further_costs,
                          :equity_ratio,
                          :debt_ratio)""",
                  {'number': bp.number,
                   'feedstock': bp.feedstock,
                   'bg_yield': bp.bg_yield,
                   'mth_yield': bp.mth_yield,
                   'dry_sub_cont': bp.dry_sub_cont,
                   'chpp_energy_supply': bp.chpp_energy_supply,
                   'ghg_avoidance': bp.ghg_avoidance,
                   'substrate_costs': bp.substrate_costs,
                   'personnel_costs': bp.personnel_costs,
                   'depreciation': bp.depreciation,
                   'maintenance_costs': bp.maintenance_costs,
                   'electricity_demand': bp.electricity_demand,
                   'heating_demand': bp.heating_demand,
                   'further_costs': bp.further_costs,
                   'equity_ratio': bp.equity_ratio,
                   'debt_ratio': bp.debt_ratio
                   })


# function to remove biogas plant from database
def remove_biogas_plant(number):
    with conn:
        c.execute("DELETE from BiogasPlants WHERE number = :number", {'number': number})


# function to select biogas plant out of database
def get_biogas_plant(number):
    with conn:
        c.execute("SELECT * from BiogasPlants WHERE number = :number", {'number': number})


# function for showing an overview over certain biogas plant
def show_parameters_biogas_plant(number):
    get_biogas_plant(number)
    b = c.fetchone()
    print(f"Number:  {b[0]} \n"
          f"Feedstock: {b[1]} t/a \n"
          f"Biogas yield: {b[2]} m³/t \n"
          f"Methane yield: {b[3]} m³/t \n"
          f"Dry substrate content: {b[4]} % \n"
          f"CHPP energy supply: {b[5]} kWh \n"
          f"GHG-avoidance: {b[6]} % \n"
          f"Substrate costs: {b[7]} €/a\n"
          f"Personell costs: {b[8]} €/a\n"
          f"Maintenance costs: {b[9]} €/a\n"
          f"Depraciation: {b[10]} €/a\n"
          f"Electricity demand: {b[11]} kWh/a\n"
          f"Heating demand: {b[12]} kWh/a\n"
          f"Further costs: {b[13]} €/a\n"
          f"Equity ratio: {b[14]} %\n"
          f"Debt ratio: {b[15]} %")


# set biogas plant parameters
def set_biogas_plant(number):
    with conn:
        c.execute("SELECT * from BiogasPlants WHERE number = :number", {'number': number})
        b = c.fetchone()
        bp = BiogasPlant(number=b[0],
                         feedstock=b[1],
                         bg_yield=b[2],
                         mth_yield=b[3],
                         dry_sub_cont=b[4],
                         chpp_energy_supply=b[5],
                         ghg_avoidance=b[6],
                         substrate_costs=b[7],
                         personnel_costs=b[8],
                         maintenance_costs=b[9],
                         depreciation=b[10],
                         electricity_demand=b[11],
                         heating_demand=b[12],
                         further_costs=b[13],
                         equity_ratio=b[14],
                         debt_ratio=b[15])
        return bp
  
# data = pd.read_excel('BMP3_Daten.xlsx')   
# choose biogas plant ( i = 1, 3, 4, 6, 8 - 11, 14, 16, 18, 22, 27-29, 31, 33, 35, 37, 40, 42, 42, 47, 48, 51, 52, 54, 56, 57, 59)

  # bp59 = BiogasPlant(number= i,
  #                   feedstock= data.loc[i -1,"Jahresmenge [t/a]"],
  #                   bg_yield=data.loc[i -1,"Biogasausbeute [m^3/t]"],
  #                   mth_yield=data.loc[i -1,"Methanausbeute [m^3/t]"],
  #                   dry_sub_cont=data.loc[i -1,"TS-Gehalt in FM [%]"],
  #                   chpp_energy_supply=data.loc[i -1,"elekt. Nennleistung [kW]"],
  #                   ghg_avoidance=data.loc[i -1,"ghg_avoidance"],
  #                   substrate_costs=data.loc[i -1,"Substratkosten [€/a]"],
  #                   personnel_costs=data.loc[i -1,"Personalkosten [€/a]"],
  #                   maintenance_costs=data.loc[i -1,"Instandhaltungskosten [€/a]"],
  #                   depreciation=data.loc[i -1,"Abschreibung [€/a]"],
  #                   electricity_demand=data.loc[i -1,"Strombedraf [kWh/a]"],
  #                   heating_demand=data.loc[i -1,"Wärmebedarf BGA [kWh/a]"],
  #                   further_costs=data.loc[i -1,"Sonstige Betriebskosten  [€/a]"],
  #                   equity_ratio = 30.3,
  #                   debt_ratio = 69.7)

  # insert_biogas_plant(bp59) 

#example for bp 11
# bp11 = BiogasPlant(number=11,
#                     feedstock=8872,
#                     bg_yield=223,
#                     mth_yield=121,
#                     dry_sub_cont=38.7,
#                     chpp_energy_supply=537,
#                     ghg_avoidance=65.2,
#                     substrate_costs=343432,
#                     personnel_costs=33841,
#                     maintenance_costs=139384,
#                     depreciation=132609,
#                     electricity_demand=370923,
#                     heating_demand=127530,
#                     further_costs=181965,
#                     equity_ratio = 30.3,
#                     debt_ratio = 69.7)

# insert_biogas_plant(bp11)

# example for bp 16
# bp16 = BiogasPlant(number=16,
#                     feedstock=36795,
#                     bg_yield=90,
#                     mth_yield=46,
#                     dry_sub_cont=17.6,
#                     chpp_energy_supply=740,
#                     ghg_avoidance=90,
#                     substrate_costs=241158,
#                     personnel_costs=52426,
#                     maintenance_costs=129000,
#                     depreciation=292979,
#                     electricity_demand=247032,
#                     heating_demand=1095542,
#                     further_costs=269157,
#                     equity_ratio =30.3,
#                     debt_ratio =69.7)

# insert_biogas_plant(bp16)
