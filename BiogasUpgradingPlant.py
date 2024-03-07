import BiogasPlant
import PARAMETER


class BiogasUpgradingPlant:
    def __init__(self, BiogasPlant, name):
        self.BiogasPlant = BiogasPlant
        self.name = name

    # define parameters for each biogas upgrading process, taken from [4]
    def get_operators(self):
        if(self.name =="AS"):
            staff_expenses = 0.5 # h/d
            electrical_demand = 0.09 # kWh/m³ raw biogas
            heat_demand = 0.6 # kWh/m³ raw biogas
            purity = 95 # %
            methane_losses = 0.1 # %
        elif(self.name == "M1"):
            staff_expenses = 0.5
            electrical_demand = 0.28
            heat_demand = 0
            purity = 97
            methane_losses = 0.3
        elif(self.name == "M2"):
            staff_expenses = 1.0
            electrical_demand = 0.195
            heat_demand = 0
            purity = 97
            methane_losses = 0.5
        elif(self.name == "PWS"):
            staff_expenses = 0.68
            electrical_demand = 0.23
            heat_demand = 0
            purity = 96
            methane_losses = 1
        elif(self.name == "PGS"):
            staff_expenses = 0.75
            electrical_demand = 0.25
            heat_demand = 0
            purity = 97
            methane_losses = 0.5
        elif(self.name == "PSA"):
            staff_expenses = 0.3
            electrical_demand = 0.2
            heat_demand = 0
            purity = 97
            methane_losses = 2.2
        return {"staff expenses": staff_expenses,
                "electrical demand": electrical_demand,
                "heat demand": heat_demand,
                "purity": purity,
                "loss": methane_losses}

    # Nm³ / a
    def get_biomethane(self):
        biomethane = self.BiogasPlant.get_total_methane() * \
                     (100-self.get_operators().get("loss"))/self.get_operators().get("purity")
        return round(biomethane)

    # m³
    def get_storage_capacity(self):
        capacity = self.get_biomethane() / 52 / PARAMETER.STORAGE_PRESSURE
        return round(capacity, 2)

    # € / a with scaling factor
    def get_dehumidification_costs(self):
        capital_costs = 37352 * (self.BiogasPlant.chpp_energy_supply/750) ** \
                        PARAMETER.SCALING_FACTOR_DEHUMIDIFICATION * \
                        (1 + PARAMETER.INFLATION_RATE) ** \
                        (PARAMETER.YEAR - 2017)
        maintenance_costs = capital_costs * PARAMETER.MAINTENANCE_RATE
        insurance_costs = capital_costs * PARAMETER.INSURANCE_RATE
        interest_costs = capital_costs * self.BiogasPlant.get_mixed_cost_interest_rate()
        total_costs = capital_costs + maintenance_costs + insurance_costs + interest_costs
        return round(total_costs, 2)

    # € non-linear interpolation and data taken from [4]
    def get_capital_costs(self):
        x = self.BiogasPlant.get_total_biogas()/365/24
        if(self.name=="AS"):
            capital_costs = 0.0000000004577*x**5 - 0.0000039703622*x**4 + 0.0105348275074*x**3 - 10.6882126738182*x**2 + 5365.8754004884 * x
        elif (self.name == "M1"):
            capital_costs = 0.0048998842593*x**3 - 10.1212523148148*x**2 + 6191.8550925925929*x
        elif (self.name == "M2"):
            capital_costs = - 0.0000000000001*x**7 + 0.0000000003445*x**6 - 0.0000004735806*x**5 + 0.0003220436513*x**4 - 0.1007307386105*x**3 + 7.6709176810896*x**2 + 4760.414672629885*x
        elif(self.name=="PWS"):
            capital_costs = 0.0000000028982*x**5 - 0.0000129785816*x**4 + 0.0203834848642*x**3 - 14.6516955326161*x**2 + 6901.2254470770777*x
        elif (self.name == "PGS"):
            capital_costs = 0.0000000000005*x**7 - 0.0000000010462*x**6 + 0.0000011830571*x**5 - 0.0007915215776*x**4 + 0.3114188232634*x**3 - 71.6714393983573*x**2 + 11488.2892079965986*x
        elif (self.name == "PSA"):
            capital_costs = - 0.0000000002331*x**6 + 0.0000005700999*x**5 - 0.0006604174402*x**4 + 0.3884725531588*x**3 - 114.4983199612913*x**2 + 17201.1701269294899*x
        capital_costs = capital_costs * (1 + PARAMETER.INFLATION_RATE) ** (PARAMETER.YEAR - 2019)
        return round(capital_costs, 2)

    # € / a data from [4]
    def get_operational_costs(self):
        labor_costs = self.get_operators().get("staff expenses") * 365 * PARAMETER.LABOR_COSTS
        electricity_costs = self.get_operators().get("electrical demand") * self.BiogasPlant.get_total_biogas() * PARAMETER.ELECTRICITY_RATE
        heating_costs = self.get_operators().get("heat demand") * self.BiogasPlant.get_total_biogas() * PARAMETER.HEATING_COSTS
        operation_costs = labor_costs + electricity_costs + heating_costs
        return round(operation_costs, 2)

    # € / a
    def get_storage_costs(self):
        capital_costs = self.get_storage_capacity() * PARAMETER.STORAGE_COSTS_BIOMETHANE
        maintenance_costs = capital_costs * PARAMETER.MAINTENANCE_RATE
        insurance_costs = capital_costs * PARAMETER.INSURANCE_RATE
        interest_costs = capital_costs * self.BiogasPlant.get_mixed_cost_interest_rate()
        total_costs = capital_costs / PARAMETER.DEPRECIATION_PERIOD + maintenance_costs + insurance_costs + interest_costs
        return round(total_costs)

    # € / a with scaling factor and data from [5]
    def get_distribution_costs(self):
        trailer_costs = 75000/PARAMETER.DEPRECIATION_PERIOD
        labor_costs = 135000
        fuel_costs = 18250
        truck_tolls = 109500
        distribution_costs_unadjusted = trailer_costs + labor_costs + fuel_costs + truck_tolls
        distribution_costs_adjusted = distribution_costs_unadjusted * (self.get_biomethane()/2332800) ** \
                                      PARAMETER.SCALING_FACTOR_DISTRIBUTION * (1 + PARAMETER.INFLATION_RATE) ** \
                                      (PARAMETER.YEAR - 2009)
        return round(distribution_costs_adjusted, 2)

    # € / a
    def get_total_costs(self):
        maintenance_costs = self.get_capital_costs() * PARAMETER.MAINTENANCE_RATE
        insurance_costs = self.get_capital_costs() * PARAMETER.INSURANCE_RATE
        interest_costs = self.get_capital_costs() * self.BiogasPlant.get_mixed_cost_interest_rate()
        if(self.name=="AS" or self.name=="M1" or self.name=="PWS"):
            total_costs = interest_costs + insurance_costs + maintenance_costs + self.get_capital_costs() / PARAMETER.DEPRECIATION_PERIOD + self.BiogasPlant.get_provision_costs_without_heating() + self.get_dehumidification_costs() + self.get_distribution_costs() + self.get_operational_costs() + self.get_storage_costs()
        elif(self.name=="M2" or self.name=="PGS" or self.name=="PSA"):
            total_costs = interest_costs + insurance_costs + maintenance_costs + self.get_capital_costs() / PARAMETER.DEPRECIATION_PERIOD + self.BiogasPlant.get_provision_costs() + self.get_dehumidification_costs() + self.get_distribution_costs() + self.get_operational_costs() + self.get_storage_costs()
        return round(total_costs)

    # t CO2 eq./ a
    def get_ghg_reduction(self):
        ghg_reduction = self.get_biomethane() * PARAMETER.CALORIFIC_VALUE_BIOMETHANE * \
                        PARAMETER.EMISSION_REFERENCE_VALUE * self.BiogasPlant.ghg_avoidance / 100 / 1000000
        return round(ghg_reduction,2)

    # € / a
    def get_qouta_revenue(self):
        ghg_reduction = self.get_biomethane() * PARAMETER.CALORIFIC_VALUE_BIOMETHANE * \
                        PARAMETER.EMISSION_REFERENCE_VALUE * self.BiogasPlant.ghg_avoidance / 100 / 1000000
        quota_revenue = ghg_reduction * PARAMETER.QUOTA_PRICE
        return round(quota_revenue)

    # € / a
    def get_sales_revenue(self):
        sales_revenue = self.get_biomethane() * PARAMETER.AVERAGE_CNG_PRICE * PARAMETER.DENSITY_H_GAS
        return round(sales_revenue)

    # € / a
    def get_total_revenue_quota(self):
        quota_revenue = self.get_qouta_revenue()
        sales_revenue = self.get_sales_revenue()
        taxes = self.get_biomethane() * PARAMETER.CALORIFIC_VALUE_BIOMETHANE * PARAMETER.ENERGY_TAXES_GAS / 3600
        total_revenue = quota_revenue + sales_revenue - taxes
        return round(total_revenue)

    # € / a
    def get_total_revenue_taxes(self):
        sales_revenue = self.get_sales_revenue()
        taxes = self.get_biomethane() * PARAMETER.CALORIFIC_VALUE_BIOMETHANE * PARAMETER.ENERGY_TAXES_GAS_CONCESSIONARY / 3600
        total_revenue = sales_revenue - taxes
        return round(total_revenue)



