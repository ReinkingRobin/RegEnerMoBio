import PARAMETER
import scipy.interpolate


class BiogasPlant:
    def __init__(self, number, feedstock, bg_yield, mth_yield, dry_sub_cont, chpp_energy_supply, ghg_avoidance,
                 substrate_costs, personnel_costs, maintenance_costs, depreciation, electricity_demand, heating_demand,
                 further_costs, equity_ratio, debt_ratio):
        self.number = number  # number of BP from 'Biogas-Messprogramm III'
        self.feedstock = feedstock  # t/a; available at Biogas-Messprogramm III
        self.bg_yield = bg_yield  # m³/t; available at Biogas-Messprogramm III
        self.mth_yield = mth_yield  # m³/t; available at Biogas-Messprogramm III
        self.dry_sub_cont = dry_sub_cont  # %; available at Biogas-Messprogramm III
        self.chpp_energy_supply = chpp_energy_supply  # kWh; available at Biogas-Messprogramm III
        self.ghg_avoidance = ghg_avoidance  # calculate from RED II
        self.substrate_costs = substrate_costs  # €/a; available at Biogas-Messprogramm III
        self.personnel_costs = personnel_costs  # €/a; available at Biogas-Messprogramm III
        self.maintenance_costs = maintenance_costs  # €/a; available at Biogas-Messprogramm III
        self.depreciation = depreciation  # €/a; available at Biogas-Messprogramm III
        self.electricity_demand = electricity_demand  # kWh/a; available at Biogas-Messprogramm III
        self.heating_demand = heating_demand  # kWh/a; available at Biogas-Messprogramm III
        self.further_costs = further_costs  # €/a; available at Biogas-Messprogramm III
        self.equity_ratio = equity_ratio  # % available at Biogas-Messprogramm III
        self.debt_ratio = debt_ratio  # % available at Biogas-Messprogramm III

    def get_total_biogas(self):  # Nm³/a
        total_bg = self.feedstock * self.bg_yield
        return total_bg

    def get_total_methane(self):  # Nm³/a
        total_mth = self.feedstock * self.mth_yield
        return total_mth

    def get_provision_costs(self):  # €/a for biogas provision after Biogas-Messprogramm III
        new_depreciation = 0
        dismantling_costs = self.get_chpp_dismantling_costs() / PARAMETER.DEPRECIATION_PERIOD
        interest_dismantling = self.get_chpp_dismantling_costs() * self.get_mixed_cost_interest_rate()
        electricity_costs = PARAMETER.ELECTRICITY_RATE * self.electricity_demand
        heating_costs = PARAMETER.HEATING_COSTS * self.heating_demand
        new_maintenance_costs = 2 * self.maintenance_costs * (1 + PARAMETER.INFLATION_RATE) ** (PARAMETER.YEAR - 2017)
        total_costs = self.substrate_costs * (1 + PARAMETER.INFLATION_RATE) ** (PARAMETER.YEAR - 2017) + \
                      self.personnel_costs * (1 + PARAMETER.INFLATION_RATE) ** (PARAMETER.YEAR - 2017) + \
                      new_maintenance_costs + \
                      new_depreciation + \
                      electricity_costs + \
                      heating_costs + \
                      dismantling_costs + \
                      interest_dismantling + \
                      self.further_costs * (1 + PARAMETER.INFLATION_RATE) ** (PARAMETER.YEAR - 2017)
        return round(total_costs)

    def get_provision_costs_without_heating(self):  # € / a; relevant if heat can be provided by further processing paths, i.e. AS
        new_depreciation = 0
        dismantling_costs = self.get_chpp_dismantling_costs() / PARAMETER.DEPRECIATION_PERIOD
        interest_dismantling = self.get_chpp_dismantling_costs() * self.get_mixed_cost_interest_rate()
        electricity_costs = PARAMETER.ELECTRICITY_RATE * self.electricity_demand
        new_maintenance_costs = 2 * self.maintenance_costs * (1 + PARAMETER.INFLATION_RATE) ** (PARAMETER.YEAR - 2017)
        total_costs = self.substrate_costs * (1 + PARAMETER.INFLATION_RATE) ** (PARAMETER.YEAR - 2017) + \
                      self.personnel_costs * (1 + PARAMETER.INFLATION_RATE) ** (PARAMETER.YEAR - 2017) + \
                      new_maintenance_costs + \
                      new_depreciation + \
                      electricity_costs + \
                      dismantling_costs + \
                      interest_dismantling + \
                      self.further_costs * (1 + PARAMETER.INFLATION_RATE) ** (PARAMETER.YEAR - 2017)
        return round(total_costs)

    def get_mixed_cost_interest_rate(self): # mixed cost approach, equity and debt ratio available at Biogas-Messprogramm III
        mixed_cost_interest = (self.equity_ratio * 0.1 + self.debt_ratio * 0.0375) / 100
        return round(mixed_cost_interest, 3)

    def get_chpp_dismantling_costs(self): # calculated with interpolation and data from [4]
        energy = [35, 50, 100, 150, 200, 250, 300, 400, 600, 800, 1200, 1560, 2000]
        costs = [90000, 110000, 130000, 180000, 230000, 250000, 320000, 400000, 460000, 510000, 550000, 700000, 780000]
        y = scipy.interpolate.interp1d(energy, costs)
        z = y(self.chpp_energy_supply) * 0.02
        return z
