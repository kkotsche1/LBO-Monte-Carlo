# distribution_utils.py

from scipy.stats import triang, norm

def setup_distributions(cases):
    """
    Set up probability distributions for the input variables using the Bear Case, Primary Case, and Management Case cases.
    """

    # Helper function to create a triangular distribution
    def create_triangular_dist(bear, base, bull):
        min_val = min(bear, base, bull)
        max_val = max(bear, base, bull)
        mode = base
        scale = max_val - min_val
        if scale <= 0:
            raise ValueError("Invalid distribution parameters: scale must be positive.")
        return triang(c=(mode - min_val) / scale, loc=min_val, scale=scale)

    # Revenue growth distribution using Bear Case, Primary Case, and Management Case case data
    revenue_growth_dist = create_triangular_dist(
        bear=cases['Bear Case'].revenue_growth[min(cases['Bear Case'].revenue_growth.keys())],
        base=cases['Primary Case'].revenue_growth[min(cases['Primary Case'].revenue_growth.keys())],
        bull=cases['Management Case'].revenue_growth[min(cases['Management Case'].revenue_growth.keys())]
    )

    ebitda_margin_dist = create_triangular_dist(
        bear=cases['Bear Case'].ebitda_margin[min(cases['Bear Case'].ebitda_margin.keys())],
        base=cases['Primary Case'].ebitda_margin[min(cases['Primary Case'].ebitda_margin.keys())],
        bull=cases['Management Case'].ebitda_margin[min(cases['Management Case'].ebitda_margin.keys())]
    )

    depreciation_percent_dist = norm(loc=cases['Primary Case'].depreciation_percent[min(cases['Primary Case'].depreciation_percent.keys())], scale=0.01)
    amortization_percent_dist = norm(loc=cases['Primary Case'].amortization_percent[min(cases['Primary Case'].amortization_percent.keys())], scale=0.01)
    m_capex_percent_dist = norm(loc=cases['Primary Case'].m_capex_percent[min(cases['Primary Case'].m_capex_percent.keys())], scale=0.01)
    e_capex_percent_dist = norm(loc=cases['Primary Case'].e_capex_percent[min(cases['Primary Case'].e_capex_percent.keys())], scale=0.01)

    inventory_percent_dist = norm(loc=cases['Primary Case'].inventory_percent[min(cases['Primary Case'].inventory_percent.keys())], scale=0.01)
    accounts_receivable_percent_dist = norm(loc=cases['Primary Case'].accounts_receivable_percent[min(cases['Primary Case'].accounts_receivable_percent.keys())], scale=0.01)
    accounts_payable_percent_dist = norm(loc=cases['Primary Case'].accounts_payable_percent[min(cases['Primary Case'].accounts_payable_percent.keys())], scale=0.01)
    other_wc_assets_percent_dist = norm(loc=cases['Primary Case'].other_wc_assets_percent[min(cases['Primary Case'].other_wc_assets_percent.keys())], scale=0.01)
    other_wc_liabilities_percent_dist = norm(loc=cases['Primary Case'].other_wc_liabilities_percent[min(cases['Primary Case'].other_wc_liabilities_percent.keys())], scale=0.01)

    # TODO dynamic exit multiple
    exit_multiple_dist = create_triangular_dist(
        bear=8,
        base=10,
        bull=12
    )

    return {
        'revenue_growth': revenue_growth_dist,
        'ebitda_margin': ebitda_margin_dist,
        'depreciation_percent': depreciation_percent_dist,
        'amortization_percent': amortization_percent_dist,
        'm_capex_percent': m_capex_percent_dist,
        'e_capex_percent': e_capex_percent_dist,
        'inventory_percent': inventory_percent_dist,
        'accounts_receivable_percent': accounts_receivable_percent_dist,
        'accounts_payable_percent': accounts_payable_percent_dist,
        'other_wc_assets_percent': other_wc_assets_percent_dist,
        'other_wc_liabilities_percent': other_wc_liabilities_percent_dist,
        'exit_multiple': exit_multiple_dist,
    }
