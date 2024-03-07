from BiogasPlant import BiogasPlant
from BiogasUpgradingPlant import BiogasUpgradingPlant
from SteamReformer import SteamReformer
from FischerTropschSynthesis import FischerTropschSynthesis
import PARAMETER
import SQLiteBiogasPlant



a = 31
# define reference plant
# 1, 3, 4, 6, 8 - 11, 14, 16, 18, 22, 27-29, 31, 33, 35, 37, 40, 42, 42, 47, 48, 51, 52, 54, 56, 57, 59
bp11 = SQLiteBiogasPlant.set_biogas_plant(a)
biogas_production = bp11.get_total_biogas()
methane_production = bp11.get_total_methane()
print("Biogas plant:")
print(f"Biogas production = {biogas_production} m³/a")
print(f"Methane production = {methane_production} m³/a")

# upgrading methods
amine_scrubbing = BiogasUpgradingPlant(BiogasPlant=bp11, name="AS")
membrane_1 = BiogasUpgradingPlant(BiogasPlant=bp11, name="M1")
membrane_2 = BiogasUpgradingPlant(BiogasPlant=bp11, name="M2")
pws = BiogasUpgradingPlant(BiogasPlant=bp11, name="PWS")
pgs = BiogasUpgradingPlant(BiogasPlant=bp11, name ="PGS")
psa = BiogasUpgradingPlant(BiogasPlant=bp11, name="PSA")
print("\nUpgrading Methods:")
print(f"Amine Scrubbing Biomethane flow = {amine_scrubbing.get_biomethane()} m³/a")
print(f"Membrane 1 Biomethane flow = {membrane_1.get_biomethane()} m³/a")
print(f"Membrane 2 Biomethane flow = {membrane_2.get_biomethane()} m³/a")
print(f"Pressurized Waser Scrubbing Biomethane flow = {pws.get_biomethane()} m³/a")
print(f"Polyethylene Glycol Scrubbing Biomethane flow = {pgs.get_biomethane()} m³/a")
print(f"Pressure Swing Adsorption Biomethane flow = {psa.get_biomethane()} m³/a")

# steam reforming
steam_reforming = SteamReformer(BiogasPlant=bp11, main_substrate="corn")
print("\nSteam Reforming:")
print(f"Hydrogen Flow = {steam_reforming.get_hydrogen_flow()} m³/a")
print(f"Hydrogen Mass = {steam_reforming.get_hydrogen_mass()} kg/d")

# fischer-tropsch synthesis
fischer_tropsch = FischerTropschSynthesis(BiogasPlant=bp11)
print("\nFischer-Tropsch Synthesis:")
print(f"Liquid Fuel production = {fischer_tropsch.get_sf_volume()} m³/a")

# economic BP11
print("\nEconomy Biogas Plant:")
print(f"Biogas provision costs = {bp11.get_provision_costs()} €/a")
print(f"Biogas provision costs without heating = {bp11.get_provision_costs_without_heating()} €/a")

# economic biogas upgrading
print("\nCosts Biogas Upgrading:")
print(f"Amine Scrubbing costs = {amine_scrubbing.get_total_costs()} €/a")
print(f"Membrane 1 costs = {membrane_1.get_total_costs()} €/a")
print(f"Membrane 2 costs = {membrane_2.get_total_costs()} €/a")
print(f"Pressurized Waser Scrubbing costs = {pws.get_total_costs()} €/a")
print(f"Polyethylene Glycol Scrubbing costs = {pgs.get_total_costs()} €/a")
print(f"Pressure Swing Adsorption costs = {psa.get_total_costs()} €/a")
print("\nRevenue Biogas Upgrading:")
print(f"Amine Scrubbing revenue with quota = {amine_scrubbing.get_total_revenue_quota()} €/a")
print(f"Membrane 1 revenue with quota = {membrane_1.get_total_revenue_quota()} €/a")
print(f"Membrane 2 revenue with quota = {membrane_2.get_total_revenue_quota()} €/a")
print(f"Pressurized Waser Scrubbing revenue with quota = {pws.get_total_revenue_quota()} €/a")
print(f"Polyethylene Glycol Scrubbing revenue with quota = {pgs.get_total_revenue_quota()} €/a")
print(f"Pressure Swing Adsorption revenue with quota = {psa.get_total_revenue_quota()} €/a")
print(f"Amine Scrubbing revenue concessionary taxes = {amine_scrubbing.get_total_revenue_taxes()} €/a")
print(f"Membrane 1 revenue concessionary taxes = {membrane_1.get_total_revenue_taxes()} €/a")
print(f"Membrane 2 revenue concessionary taxes = {membrane_2.get_total_revenue_taxes()} €/a")
print(f"Pressurized Waser Scrubbing revenue concessionary taxes = {pws.get_total_revenue_taxes()} €/a")
print(f"Polyethylene Glycol Scrubbing revenue concessionary taxes = {pgs.get_total_revenue_taxes()} €/a")
print(f"Pressure Swing Adsorption revenue concessionary taxes = {psa.get_total_revenue_taxes()} €/a")
print("\nBalance Biogas Upgrading:")
print(f"Amine Scrubbing balance with quota = {amine_scrubbing.get_total_revenue_quota()-amine_scrubbing.get_total_costs()} €/a")
print(f"Membrane 1 balance with quota = {membrane_1.get_total_revenue_quota()-membrane_1.get_total_costs()} €/a")
print(f"Membrane 2 balance with quota = {membrane_2.get_total_revenue_quota()-membrane_2.get_total_costs()} €/a")
print(f"Pressurized Waser Scrubbing balance with quota = {pws.get_total_revenue_quota()-pws.get_total_costs()} €/a")
print(f"Polyethylene Glycol Scrubbing balance with quota = {pgs.get_total_revenue_quota()-pgs.get_total_costs()} €/a")
print(f"Pressure Swing Adsorption balance with quota = {psa.get_total_revenue_quota()-psa.get_total_costs()} €/a")
print(f"Amine Scrubbing balance concessionary taxes = {amine_scrubbing.get_total_revenue_taxes()-amine_scrubbing.get_total_costs()} €/a")
print(f"Membrane 1 balance concessionary taxes = {membrane_1.get_total_revenue_taxes()-membrane_1.get_total_costs()} €/a")
print(f"Membrane 2 balance concessionary taxes = {membrane_2.get_total_revenue_taxes()-membrane_2.get_total_costs()} €/a")
print(f"Pressurized Waser Scrubbing balance concessionary taxes = {pws.get_total_revenue_taxes()-pws.get_total_costs()} €/a")
print(f"Polyethylene Glycol Scrubbing balance concessionary taxes = {pgs.get_total_revenue_taxes()-pgs.get_total_costs()} €/a")
print(f"Pressure Swing Adsorption balance concessionary taxes = {psa.get_total_revenue_taxes()-psa.get_total_costs()} €/a")

# economic steam reforming
print("\nEconomy Steam Reforming:")
print(f"Steam Reforming costs = {steam_reforming.get_total_costs()} €/a")
print(f"Steam Reforming revenue quota = {steam_reforming.get_total_revenue_quota()} €/a")
print(f"Steam Reforming revenue taxes = {steam_reforming.get_total_revenue_taxes()} €/a")
print(f"Steam Reforming balance quota = {steam_reforming.get_total_revenue_quota()-steam_reforming.get_total_costs()} €/a")
print(f"Steam Reforming balance taxes = {steam_reforming.get_total_revenue_taxes()-steam_reforming.get_total_costs()} €/a")

# economic fischer-tropsch
print("\nEconomy Fischer-Tropsch Synthesis:")
print(f"FTS costs = {fischer_tropsch.get_total_costs()} €/a")
print(f"FTS revenue with quota = {fischer_tropsch.get_total_revenue_with_quota()} €/a")
print(f"FTS revenue without quota = {fischer_tropsch.get_total_revenue_without_quota()} €/a")
print(f"FTS balance with quota = {fischer_tropsch.get_total_revenue_with_quota()-fischer_tropsch.get_total_costs()} €/a")
print(f"FTS balance without quota = {fischer_tropsch.get_total_revenue_without_quota()-fischer_tropsch.get_total_costs()} €/a")


SQLiteBiogasPlant.conn.commit()
SQLiteBiogasPlant.conn.close()
