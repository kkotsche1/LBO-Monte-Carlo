# monte_carlo.py

import numpy as np
import pandas as pd
from lbo_run import run_lbo_model_with_repayment_schedule
from monte_carlo_distributions import setup_distributions
import matplotlib.pyplot as plt
from tqdm import tqdm

class MonteCarloSimulator:
    def __init__(self, cases, deal_metrics, repayment_schedule, years, iterations=1000, exit_horizons=None):
        """
        Initialize the Monte Carlo simulator with all three cases (Bear, Base, Bull).
        Only run simulations for the exit horizon years.
        """
        self.cases = cases  # Dictionary with 'Bear', 'Base', and 'Bull' case data
        self.deal_metrics = deal_metrics
        self.repayment_schedule = repayment_schedule
        self.years = years
        self.iterations = iterations
        self.exit_horizons = exit_horizons if exit_horizons else [2026, 2027, 2028, 2029]
        self.distributions = setup_distributions(cases)  # Pass all cases to setup the distributions

    def run_simulation(self):
        results = []

        for i in tqdm(range(self.iterations)):
            # Generate random variables based on distributions
            random_inputs = {
                'revenue_growth': self.distributions['revenue_growth'].rvs(),
                'ebitda_margin': self.distributions['ebitda_margin'].rvs(),
                'depreciation_percent': self.distributions['depreciation_percent'].rvs(),
                'amortization_percent': self.distributions['amortization_percent'].rvs(),
                'm_capex_percent': self.distributions['m_capex_percent'].rvs(),
                'e_capex_percent': self.distributions['e_capex_percent'].rvs(),
                'inventory_percent': self.distributions['inventory_percent'].rvs(),
                'accounts_receivable_percent': self.distributions['accounts_receivable_percent'].rvs(),
                'accounts_payable_percent': self.distributions['accounts_payable_percent'].rvs(),
                'other_wc_assets_percent': self.distributions['other_wc_assets_percent'].rvs(),
                'other_wc_liabilities_percent': self.distributions['other_wc_liabilities_percent'].rvs(),
                'exit_multiple': self.distributions['exit_multiple'].rvs(),
            }

            # Use the 'Base' case as a starting point and modify it with random inputs
            case_data_randomized = self.modify_case_data(random_inputs)

            # Run the LBO model for the exit horizon years only
            result = run_lbo_model_with_repayment_schedule(
                self.deal_metrics, case_data_randomized, self.repayment_schedule, self.years, exit_horizons=self.exit_horizons
            )

            # Collect results for each exit horizon (e.g., IRR, MoM, etc.)
            for exit_year in self.exit_horizons:
                if exit_year in result:
                    results.append(result[exit_year])

        return pd.DataFrame(results)

    def modify_case_data(self, random_inputs):
        # Use the 'Base' case as the starting point
        base_case = self.cases['Primary Case']

        # Make a deep copy of the Base case data
        case_data_randomized = base_case.__class__(
            name=base_case.name,
            revenue=base_case.revenue.copy(),
            ebitda=base_case.ebitda.copy(),
            ebitda_normalizations=base_case.ebitda_normalizations.copy(),
            depreciation=base_case.depreciation.copy(),
            amortization=base_case.amortization.copy(),
            ebit=base_case.ebit.copy(),
            maintenance_capex=base_case.maintenance_capex.copy(),
            expansion_capex=base_case.expansion_capex.copy(),
            inventory=base_case.inventory.copy(),
            accounts_receivable=base_case.accounts_receivable.copy(),
            accounts_payable=base_case.accounts_payable.copy(),
            other_wc_assets=base_case.other_wc_assets.copy(),
            other_wc_liabilities=base_case.other_wc_liabilities.copy(),
            provisions=base_case.provisions.copy(),
            revenue_growth=base_case.revenue_growth.copy(),
            ebitda_margin=base_case.ebitda_margin.copy(),
            depreciation_percent=base_case.depreciation_percent.copy(),
            amortization_percent=base_case.amortization_percent.copy(),
            ebit_margin=base_case.ebit_margin.copy(),
            m_capex_percent=base_case.m_capex_percent.copy(),
            e_capex_percent=base_case.e_capex_percent.copy(),
            inventory_percent=base_case.inventory_percent.copy(),
            accounts_receivable_percent=base_case.accounts_receivable_percent.copy(),
            accounts_payable_percent=base_case.accounts_payable_percent.copy(),
            other_wc_assets_percent=base_case.other_wc_assets_percent.copy(),
            other_wc_liabilities_percent=base_case.other_wc_liabilities_percent.copy(),
            provisions_growth=base_case.provisions_growth.copy(),
        )

        # Apply randomizations to the relevant financial variables for each year
        for year in self.years:
            # Randomize revenue based on the growth rate
            if year in case_data_randomized.revenue:
                case_data_randomized.revenue[year] *= (1 + random_inputs['revenue_growth'])

            # Apply the random EBITDA margin
            if year in case_data_randomized.ebitda_margin:
                case_data_randomized.ebitda_margin[year] = random_inputs['ebitda_margin']

            # Apply random values to other financial ratios and metrics
            case_data_randomized.depreciation_percent[year] = random_inputs['depreciation_percent']
            case_data_randomized.amortization_percent[year] = random_inputs['amortization_percent']
            case_data_randomized.m_capex_percent[year] = random_inputs['m_capex_percent']
            case_data_randomized.e_capex_percent[year] = random_inputs['e_capex_percent']
            case_data_randomized.inventory_percent[year] = random_inputs['inventory_percent']
            case_data_randomized.accounts_receivable_percent[year] = random_inputs['accounts_receivable_percent']
            case_data_randomized.accounts_payable_percent[year] = random_inputs['accounts_payable_percent']
            case_data_randomized.other_wc_assets_percent[year] = random_inputs['other_wc_assets_percent']
            case_data_randomized.other_wc_liabilities_percent[year] = random_inputs['other_wc_liabilities_percent']

        return case_data_randomized

    import matplotlib.pyplot as plt

    def analyze_results(self, results_df):
        # Plot the IRR distribution if available
        if 'IRR' in results_df.columns:
            results_df['IRR'].hist(bins=50)
            plt.title("Distribution of IRRs from Monte Carlo Simulation")
            plt.xlabel("IRR (%)")
            plt.ylabel("Frequency")
            plt.show()

            print(results_df['IRR'].describe())  # Get basic statistics like mean, std, etc.
        else:
            print("No IRR data found in the results.")

        # Plot the MoM distribution if available
        if 'MoM' in results_df.columns:
            results_df['MoM'].hist(bins=50)
            plt.title("Distribution of MoM (Multiple on Money) from Monte Carlo Simulation")
            plt.xlabel("MoM")
            plt.ylabel("Frequency")
            plt.show()

            print(results_df['MoM'].describe())  # Get basic statistics like mean, std, etc.)
        else:
            print("No MoM data found in the results.")
