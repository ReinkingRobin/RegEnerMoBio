# Economic analysis
EMISSION_REFERENCE_VALUE = 94.1  # g CO2-eq./MJ
ENERGY_TAX_RATE_DIESEL = 0.4704  # €/L
ENERGY_TAXES_GAS_CONCESSIONARY = 13.9  # €/MWh
ENERGY_TAXES_GAS = 31.8  # €/MWh
QUOTA_PRICE = 250  # €/t
DEPRECIATION_PERIOD = 15  # a
INFLATION_RATE = 0.01  # assumption taken from [4]
YEAR = 2021  # reference year
INSURANCE_RATE = 0.005  # assumption taken from [4]
SCALING_FACTOR_FARM_STATION = 1
MAINTENANCE_RATE = 0.02  # assumption taken from [4]
LABOR_COSTS = 31.28  # €/h inflation adjusted
ELECTRICITY_RATE = 0.23  # €/kWh
HEATING_COSTS = 0.08  # €/kWh
AVERAGE_DIESEL_PRICE = 1.7  # €/L


# Purification and upgrading
STORAGE_COSTS_BIOMETHANE = 65  # €/Nm³ storage capacity
CALORIFIC_VALUE_BIOMETHANE = 36.97  # MJ/m³
DENSITY_H_GAS = 0.79  # kg/m³
AVERAGE_CNG_PRICE = 1.1  # €/kg
STORAGE_PRESSURE = 10  # bar
SCALING_FACTOR_DISTRIBUTION = 0.9  # assumption from literature data specified in thesis
SCALING_FACTOR_DEHUMIDIFICATION = 0.3643  # calculated with linear interpolation

# Steam reforming
SCALING_FACTOR_SR = 0.7  # assumption from literature data specified in thesis
COMPRESSION_COSTS = 0.5  # €/kg non-inflation adjusted
TRANSPORTATION_COSTS = 0.86  # €/kg non-inflation adjusted; for 150 km
STORAGE_COSTS_HYDROGEN = 0.14  # €/kg non-inflation adjusted
DISTRIBUTION_COSTS = 1.17  # €/kg non-inflation adjusted
CALORIFIC_VALUE_HYDROGEN = 123  # MJ/kg
AVERAGE_HYDROGEN_PRICE = 9.5  # €/kg
HYDROGEN_PRODUCTION_RATE_CORN = 0.65  # Nm³/kg dry substrate
HYDROGEN_PRODUCTION_RATE_POTATO = 0.59  # Nm³/kg dry substrate
HYDROGEN_PRODUCTION_RATE_GREEN_CUTTINGS = 0.62  # Nm³/kg dry substrate
HYDROGEN_PRODUCTION_RATE_ORGANIC_WASTE = 0.3  # Nm³/kg dry substrate
DENSITY_HYDROGEN = 0.08988  # g/m³ at 273K


# FTS
CALORIFIC_VALUE_DIESEL = 43.3  # MJ/kg
DENSITY_SF = 0.87474  # kg/L
SCALING_FACTOR_FTS = 0.8  # assumption from literature data specified in thesis
METHANE_DENSITY = 0.69  # kg/m³
MOLAR_MASS_HYDROGEN = 2  # g/mol
MOLAR_MASS_METHANE = 18  # g/mol
MOLAR_MASS_CARBONMONOOXIDE = 28  # g/mol
HYDROGEN_METHANE_RATIO = 3  # based on stoichiometry from methane steam reforming
CARBONMONOOXIDE_METHANE_RATIO = 1  # based on stoichiometry from methane steam reforming
REACTION_CONVERSION_EFFICIENCY = 1  # best case scenario
FTS_CONVERSION_EFFICIENCY = 0.33  # assumption from [9]
