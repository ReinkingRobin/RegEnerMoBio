from BiogasPlant import BiogasPlant
import PARAMETER


class FischerTropschSynthesis:
    def __init__(self, BiogasPlant):
        self.BiogasPlant = BiogasPlant

    # m³ / a data and formulas from [9]
    def get_sf_volume(self):
        methane_mass = self.BiogasPlant.get_total_methane() * PARAMETER.METHANE_DENSITY
        hydrogen_mass = PARAMETER.MOLAR_MASS_HYDROGEN / PARAMETER.MOLAR_MASS_METHANE * \
                        PARAMETER.HYDROGEN_METHANE_RATIO * methane_mass * \
                        PARAMETER.REACTION_CONVERSION_EFFICIENCY
        carbonm_mass = PARAMETER.MOLAR_MASS_CARBONMONOOXIDE / PARAMETER.MOLAR_MASS_METHANE * \
                       PARAMETER.CARBONMONOOXIDE_METHANE_RATIO * methane_mass * \
                       PARAMETER.REACTION_CONVERSION_EFFICIENCY
        lf_volume = (carbonm_mass+hydrogen_mass) * PARAMETER.FTS_CONVERSION_EFFICIENCY / PARAMETER.DENSITY_SF / 1000
        return round(lf_volume, 2)

    # € / a with scaling factor
    def get_capital_costs(self):
        scaling_factor = (self.BiogasPlant.get_total_biogas() / 860000) ** PARAMETER.SCALING_FACTOR_FTS
        capital_costs_reforming = 1586086 * scaling_factor
        capital_costs_ft = 3910170 * scaling_factor
        capital_costs_total = (capital_costs_ft + capital_costs_reforming) * \
                              (1 + PARAMETER.INFLATION_RATE) ** (PARAMETER.YEAR - 2019)
        return round(capital_costs_total, 2)

    # € / a with scaling factor
    def get_operation_maintenance_costs(self):
        scaling_factor = (self.BiogasPlant.get_total_biogas()/860000) ** PARAMETER.SCALING_FACTOR_FTS
        operation_maintenance_costs_reforming = 158601 * scaling_factor
        operation_maintenance_costs_ft = 156407 * scaling_factor
        operation_maintenance_costs_total = (operation_maintenance_costs_ft + operation_maintenance_costs_reforming) * \
                                            (1 + PARAMETER.INFLATION_RATE) ** (PARAMETER.YEAR - 2019)
        return round(operation_maintenance_costs_total, 2)

    # € / a
    def get_transportation_costs(self):
        transportation_costs = self.get_sf_volume() * PARAMETER.DENSITY_SF * (1 + PARAMETER.INFLATION_RATE) ** \
                               (PARAMETER.YEAR - 2014) * 12.48
        return round(transportation_costs, 2)

    # € / a
    def get_distribution_costs(self):
        distribution_storage_costs = 10.0097 * self.get_sf_volume() * (1 + PARAMETER.INFLATION_RATE) ** (
                    PARAMETER.YEAR - 2012)
        transportation_costs = 8.00776 * self.get_sf_volume() * (1 + PARAMETER.INFLATION_RATE) ** (
                    PARAMETER.YEAR - 2012)
        total_distribution_costs = distribution_storage_costs + transportation_costs
        return round(total_distribution_costs)

    # € / a
    def get_total_costs(self):
        capital_costs = self.get_capital_costs()
        operation_maintenance_costs = self.get_operation_maintenance_costs()
        insurance_costs = self.get_capital_costs() * PARAMETER.INSURANCE_RATE
        interest_costs = self.get_capital_costs() * self.BiogasPlant.get_mixed_cost_interest_rate()
        biogas_provision_costs = self.BiogasPlant.get_provision_costs()
        distribution_costs = self.get_distribution_costs()
        total_costs = capital_costs / PARAMETER.DEPRECIATION_PERIOD + operation_maintenance_costs + \
                      insurance_costs + interest_costs + biogas_provision_costs + distribution_costs
        return round(total_costs)

    # t CO2 eq. / a
    def get_ghg_avoidance(self):
        ghg_avoidance = self.get_sf_volume() * PARAMETER.DENSITY_SF * 1000 * PARAMETER.CALORIFIC_VALUE_DIESEL * \
                        PARAMETER.EMISSION_REFERENCE_VALUE * self.BiogasPlant.ghg_avoidance / 100 / 1000000
        return round(ghg_avoidance, 2)

    # € / a
    def get_quota_revenue(self):
        quota_revenue = self.get_ghg_avoidance() * PARAMETER.QUOTA_PRICE
        return round(quota_revenue)

    # € / a
    def get_sales_revenue(self):
        sales_revenue = PARAMETER.AVERAGE_DIESEL_PRICE * 1000 * self.get_sf_volume()
        return round(sales_revenue)

    # € / a
    def get_total_revenue_with_quota(self):
        taxes = self.get_sf_volume() * 1000 * PARAMETER.ENERGY_TAX_RATE_DIESEL
        total_revenue = self.get_quota_revenue() + self.get_sales_revenue() - taxes
        return round(total_revenue)

    # € / a
    def get_total_revenue_without_quota(self):
        taxes = self.get_sf_volume() * 1000 * PARAMETER.ENERGY_TAX_RATE_DIESEL
        total_revenue = self.get_sales_revenue() - taxes
        return round(total_revenue)

