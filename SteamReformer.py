import BiogasPlant
import PARAMETER


class SteamReformer:
    def __init__(self, BiogasPlant, main_substrate):
        self.BiogasPlant = BiogasPlant
        self.main_substrate = main_substrate

    # Nm³/a
    def get_hydrogen_flow(self):
        if self.main_substrate=="corn":
            production_rate = PARAMETER.HYDROGEN_PRODUCTION_RATE_CORN
        elif self.main_substrate== "potato":
            production_rate = PARAMETER.HYDROGEN_PRODUCTION_RATE_POTATO
        elif self.main_substrate== "green cuttings":
            production_rate = PARAMETER.HYDROGEN_PRODUCTION_RATE_GREEN_CUTTINGS
        elif self.main_substrate== "organic waste":
            production_rate = PARAMETER.HYDROGEN_PRODUCTION_RATE_ORGANIC_WASTE
        hydrogen_flow = self.BiogasPlant.dry_sub_cont / 100 * self.BiogasPlant.feedstock * 1000 * production_rate / 365
        return round(hydrogen_flow, 2)

    # kg / a
    def get_hydrogen_mass(self):
        hydrogen_mass = self.get_hydrogen_flow() * PARAMETER.DENSITY_HYDROGEN
        return round(hydrogen_mass, 2)

    # € / a
    def get_total_costs(self):
        energy_value = self.get_hydrogen_mass() * PARAMETER.CALORIFIC_VALUE_HYDROGEN / 24 / 60 / 60
        capital_costs = 11000000 * (energy_value/6) ** \
                        PARAMETER.SCALING_FACTOR_SR * (1 + PARAMETER.INFLATION_RATE) ** \
                        (PARAMETER.YEAR - 2014)
        operational_costs = 0.5 * self.get_hydrogen_mass() * 365 * (1 + PARAMETER.INFLATION_RATE) \
                            ** (PARAMETER.YEAR - 2014) * 1.2
        maintenance_costs = capital_costs * PARAMETER.MAINTENANCE_RATE
        insurance_costs = capital_costs * PARAMETER.INSURANCE_RATE
        interest_costs = capital_costs * self.BiogasPlant.get_mixed_cost_interest_rate()
        total_costs = capital_costs / PARAMETER.DEPRECIATION_PERIOD + operational_costs + \
                      maintenance_costs + insurance_costs + interest_costs + \
                      self.get_hydrogen_station_costs() + self.BiogasPlant.get_provision_costs()
        return round(total_costs)

    # € / a
    def get_hydrogen_station_costs(self):
        hydrogen_mass = self.get_hydrogen_mass()*365
        compressions_costs = hydrogen_mass * PARAMETER.COMPRESSION_COSTS
        transportation_costs = hydrogen_mass * PARAMETER.TRANSPORTATION_COSTS
        storage_costs = hydrogen_mass * PARAMETER.STORAGE_COSTS_HYDROGEN
        distribution_costs = hydrogen_mass * PARAMETER.DISTRIBUTION_COSTS
        station_costs = (compressions_costs + transportation_costs + storage_costs + distribution_costs) * \
                        (1 + PARAMETER.INFLATION_RATE) ** (PARAMETER.YEAR - 2014)
        return round(station_costs, 2)

    # t CO2 eq. / a
    def get_ghg_reduction(self):
        ghg_reduction = self.get_hydrogen_mass() * 365 * PARAMETER.CALORIFIC_VALUE_HYDROGEN * \
                        PARAMETER.EMISSION_REFERENCE_VALUE * self.BiogasPlant.ghg_avoidance / 100 / 1000000
        return round(ghg_reduction, 2)

    # € / a
    def get_quota_revenue(self):
        quota_revenue = self.get_ghg_reduction() * PARAMETER.QUOTA_PRICE
        return round(quota_revenue,2 )

    # € / a
    def get_sales_revenue(self):
        sales_revenue = self.get_hydrogen_mass() * 365 * PARAMETER.AVERAGE_HYDROGEN_PRICE
        return round(sales_revenue, 2)

    # € / a
    def get_total_revenue_quota(self):
        quota_revenue = self.get_quota_revenue()
        sales_revenue = self.get_sales_revenue()
        taxes = self.get_hydrogen_mass() * 365 * PARAMETER.CALORIFIC_VALUE_HYDROGEN * PARAMETER.ENERGY_TAXES_GAS / 3600
        total_revenue = quota_revenue + sales_revenue - taxes
        return round(total_revenue)

    # € / a
    def get_total_revenue_taxes(self):
        sales_revenue = self.get_sales_revenue()
        taxes = self.get_hydrogen_mass() * 365 * PARAMETER.CALORIFIC_VALUE_HYDROGEN * \
                PARAMETER.ENERGY_TAXES_GAS_CONCESSIONARY / 3600
        total_revenue = sales_revenue - taxes
        return round(total_revenue)



