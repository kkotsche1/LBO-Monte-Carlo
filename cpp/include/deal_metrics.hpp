// deal_metrics.hpp

#pragma once

#include <string>
#include <map>

// Structure to hold exit metrics for each period
struct ExitMetrics {
    double exit_multiple;
    double enterprise_value_exit;
    double net_debt_exit;
    double equity_value_exit;
    double mom;  // Multiple on Money
    double irr;
};

// Main structure to hold all deal metrics
struct DealMetrics {
    // Debt Information
    double senior_a_amount;
    double senior_a_interest;
    double senior_b_amount;
    double senior_b_interest;

    // Subordinate/Mezzanine Debt
    double subordinate_amount;
    double subordinate_interest;
    double mezzanine_cash_amount;
    double mezzanine_cash_interest;

    // Revolving Credit Facility (RCF)
    double rcf_amount;
    double rcf_interest;
    double rcf_undrawn_interest;

    // Equity Contributions
    double zqwl_equity;     // Replacing "GHPE Equity" with "ZQWL Equity"
    double co_invest;
    double mpp;

    // Transaction Costs
    double net_debt_at_closing;
    double restricted_cash_and_overfunding;

    // Valuation Metrics
    double entry_multiple;
    double enterprise_value_entry;

    // Exit Metrics by Period
    // Key: Period (e.g., "Entry + 3yrs"), Value: ExitMetrics struct
    std::map<std::string, ExitMetrics> exit_metrics_by_period;
};

struct ExitMetrics {
    double exit_multiple;
    double enterprise_value_exit;
    double net_debt_exit;
    double equity_value_exit;
    double mom;  // Multiple on Money
    double irr;
};
