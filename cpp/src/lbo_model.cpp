// lbo_model.cpp

#include "lbo_model.hpp"
#include "debt_calculations.hpp"
#include <algorithm>
#include <numeric>
#include <string>
#include <cmath>
#include <limits>

// Function to calculate IRR using the Newton-Raphson method
double calculate_irr(const std::vector<double>& cash_flows) {
    const double tolerance = 1e-6;
    const int max_iterations = 1000;
    double irr = 0.1;  // Initial guess

    for (int iter = 0; iter < max_iterations; ++iter) {
        double npv = 0.0;
        double npv_derivative = 0.0;

        for (size_t t = 0; t < cash_flows.size(); ++t) {
            double denominator = std::pow(1.0 + irr, t);
            if (denominator == 0.0) {
                denominator = std::numeric_limits<double>::epsilon();
            }
            double cf = cash_flows[t];
            npv += cf / denominator;
            npv_derivative -= t * cf / std::pow(1.0 + irr, t + 1);
        }

        if (std::abs(npv) < tolerance) {
            return irr;
        }

        if (npv_derivative == 0.0) {
            // Avoid division by zero
            break;
        }

        double irr_new = irr - npv / npv_derivative;

        if (std::abs(irr_new - irr) < tolerance) {
            return irr_new;
        }

        irr = irr_new;
    }

    // If convergence not achieved, return NaN
    return std::numeric_limits<double>::quiet_NaN();
}

// Implementation of the LBO model
std::map<int, std::map<std::string, double>> run_lbo_model_with_repayment_schedule(
    const DealMetrics& expanded_metrics,
    const CaseData& case_data,
    const RepaymentSchedule& repayment_schedule,
    const std::vector<int>& years,
    double tax_rate,
    const std::vector<int>& exit_horizons
) {
    std::map<int, std::map<std::string, double>> exit_results;

    // Map exit years to keys in exit_metrics_by_period
    std::map<int, std::string> exit_horizon_to_key = {
        {2026, "Entry + 3yrs"},
        {2027, "Entry + 4yrs"},
        {2028, "Entry + 5yrs"},
        {2029, "Entry + 6yrs"}
    };

    // Extract initial debt balances and interest rates from expanded_metrics
    std::map<std::string, double> starting_balances = {
        {"Senior A", expanded_metrics.senior_a_amount},
        {"Senior B", expanded_metrics.senior_b_amount},
        {"Subordinate", expanded_metrics.subordinate_amount},
        {"Mezzanine", expanded_metrics.mezzanine_cash_amount},
        {"RCF", 0.0}  // Revolver starts with a 0 balance
    };

    InterestRates interest_rates = {
        {"Senior A", expanded_metrics.senior_a_interest},
        {"Senior B", expanded_metrics.senior_b_interest},
        {"Subordinate", expanded_metrics.subordinate_interest},
        {"Mezzanine", expanded_metrics.mezzanine_cash_interest},
        {"RCF", expanded_metrics.rcf_interest}  // Interest on revolver
    };

    // Maximum revolver amount you can draw
    double max_revolver_draw = expanded_metrics.rcf_amount;

    // Calculate debt balances and interest payments
    DebtInfo debt_info = calculate_debt_balances_and_interest(
        expanded_metrics,
        repayment_schedule,
        interest_rates,
        starting_balances,
        years
    );

    double equity_investment = expanded_metrics.zqwl_equity + expanded_metrics.co_invest + expanded_metrics.mpp;
    double revolver_balance = 0.0;
    double cash_balance = 0.0;  // Initialize cash balance for the first year

    std::map<int, std::map<std::string, double>> per_year_data;

    for (size_t idx = 0; idx < years.size(); ++idx) {
        int year = years[idx];

        // Retrieve financial data for the current year
        double revenue = case_data.revenue.at(year);
        double ebitda_margin = case_data.ebitda_margin.at(year);
        double reported_ebitda = revenue * ebitda_margin;
        double ebitda_normalization = case_data.ebitda_normalizations.at(year);
        double normalized_ebitda = reported_ebitda - ebitda_normalization;

        double ebitda = normalized_ebitda;
        double depreciation = revenue * case_data.depreciation_percent.at(year);
        double amortization = revenue * case_data.amortization_percent.at(year);
        double ebit = ebitda - depreciation - amortization;

        double pik_interest = 0.0;  // Assuming PIK Interest is 0 if not provided

        // Calculate total interest expense
        double total_interest_expense = -std::accumulate(
            debt_info.begin(), debt_info.end(), 0.0,
            [year](double sum, const auto& pair) {
                const std::string& debt_type = pair.first;
                const DebtYearInfo& info = pair.second.at(year);
                return sum + info.interest_payment;
            }
        ) + pik_interest;

        double ebt = ebit + total_interest_expense;
        double taxes = std::max(0.0, ebt * tax_rate);
        double net_income = ebt - taxes;

        double change_in_nwc = 0.0;
        double change_in_provisions = 0.0;

        if (idx > 0) {
            int previous_year = years[idx - 1];

            double other_wc_assets_current = case_data.other_wc_assets_percent.at(year) * revenue;
            double other_wc_assets_previous = case_data.other_wc_assets_percent.at(previous_year) * case_data.revenue.at(previous_year);

            double other_wc_liabilities_current = -case_data.other_wc_liabilities_percent.at(year) * revenue;
            double other_wc_liabilities_previous = -case_data.other_wc_liabilities_percent.at(previous_year) * case_data.revenue.at(previous_year);

            double trade_working_capital_current = case_data.inventory.at(year) + case_data.accounts_receivable.at(year) + case_data.accounts_payable.at(year);
            double trade_working_capital_previous = case_data.inventory.at(previous_year) + case_data.accounts_receivable.at(previous_year) + case_data.accounts_payable.at(previous_year);

            double net_working_capital_current = trade_working_capital_current + other_wc_assets_current + other_wc_liabilities_current;
            double net_working_capital_previous = trade_working_capital_previous + other_wc_assets_previous + other_wc_liabilities_previous;

            change_in_nwc = net_working_capital_current - net_working_capital_previous;
            change_in_provisions = case_data.provisions.at(year) - case_data.provisions.at(previous_year);
        }

        double m_capex_percent = case_data.m_capex_percent.at(year);
        double e_capex_percent = case_data.e_capex_percent.at(year);
        double capex = revenue * m_capex_percent + revenue * e_capex_percent;

        double cfads = reported_ebitda - change_in_nwc - change_in_provisions - capex - taxes;

        double cash_interest_paid = -std::accumulate(
            debt_info.begin(), debt_info.end(), 0.0,
            [year](double sum, const auto& pair) {
                const std::string& debt_type = pair.first;
                const DebtYearInfo& info = pair.second.at(year);
                return sum + info.interest_payment;
            }
        );

        // Sum of mandatory debt repayments for the year
        double mandatory_debt_repayment = 0.0;
        for (const std::string& debt_type : {"Senior A", "Senior B", "Subordinate", "Mezzanine"}) {
            double repayment = 0.0;

            if (debt_type == "Senior A") {
                if (repayment_schedule.senior_a_repayments.count(year)) {
                    repayment = repayment_schedule.senior_a_repayments.at(year);
                }
            } else if (debt_type == "Senior B") {
                if (repayment_schedule.senior_b_repayments.count(year)) {
                    repayment = repayment_schedule.senior_b_repayments.at(year);
                }
            } else if (debt_type == "Subordinate") {
                if (repayment_schedule.subordinate_repayments.count(year)) {
                    repayment = repayment_schedule.subordinate_repayments.at(year);
                }
            } else if (debt_type == "Mezzanine") {
                if (repayment_schedule.mezzanine_repayments.count(year)) {
                    repayment = repayment_schedule.mezzanine_repayments.at(year);
                }
            }

            mandatory_debt_repayment += repayment;
        }


        // Calculate Free Cash Flow post-debt service (FCF post-debt service)
        double fcf_post_debt_service = cfads + cash_interest_paid + mandatory_debt_repayment;

        // Store the unadjusted FCF post-debt service for debugging purposes
        double original_fcf_post_debt_service = fcf_post_debt_service;

        // Revolver logic: Draw if FCF post-debt service is negative, repay if positive
        if (fcf_post_debt_service < 0.0) {
            // Draw exactly enough to cover the shortfall (bring cash balance to 0)
            double revolver_draw = -fcf_post_debt_service;  // Draw the amount needed to bring cash to zero
            revolver_balance += revolver_draw;
            cash_balance = 0.0;  // After drawing from revolver, cash balance should be exactly 0
            fcf_post_debt_service = 0.0;  // Reset FCF post revolver draw (since it's fully covered)
        } else {
            if (fcf_post_debt_service > 0.0 && revolver_balance > 0.0) {
                // Repay revolver if there is a positive FCF and an outstanding revolver balance
                double revolver_repayment = std::min(fcf_post_debt_service, revolver_balance);
                revolver_balance -= revolver_repayment;
                fcf_post_debt_service -= revolver_repayment;
                cash_balance -= revolver_repayment;  // Adjust cash balance with revolver repayment
            }

            if (fcf_post_debt_service > 0.0) {
                // Excess cash after revolver repayment, accumulate in cash balance
                cash_balance += fcf_post_debt_service;
                fcf_post_debt_service = 0.0;  // Reset after adding to cash balance
            }
        }

        // Update average revolver balance
        double average_revolver_balance = (starting_balances["RCF"] + revolver_balance) / 2.0;
        double revolver_interest = average_revolver_balance * interest_rates["RCF"];

        // Update debt_info for RCF
        DebtYearInfo& rcf_info = debt_info["RCF"][year];
        rcf_info.opening_balance = revolver_balance;
        rcf_info.closing_balance = revolver_balance;
        rcf_info.interest_payment = revolver_interest;

        per_year_data[year] = {
            {"ebitda", ebitda},
            {"cash_balance", cash_balance}
        };

        if (std::find(exit_horizons.begin(), exit_horizons.end(), year) != exit_horizons.end()) {
            double exit_multiple = expanded_metrics.exit_metrics_by_period.at(std::to_string(year)).exit_multiple;
            double ebitda_exit = per_year_data.at(year).at("ebitda");
            double enterprise_value_exit = exit_multiple * ebitda_exit;

            // Calculate total debt excluding RCF
            double total_debt = 0.0;
            for (const std::string& debt_type : {"Senior A", "Senior B", "Subordinate", "Mezzanine"}) {
                total_debt += debt_info[debt_type][year].closing_balance;
            }

            double cash_exit = per_year_data.at(year).at("cash_balance");
            double net_debt_exit = total_debt - cash_exit;

            double equity_value_exit = enterprise_value_exit - net_debt_exit;
            double mom = equity_value_exit / equity_investment;

            // Prepare cash flows for IRR calculation
            std::vector<double> cf_equity(idx + 2, 0.0);
            cf_equity[0] = -equity_investment;  // Initial investment
            cf_equity[idx + 1] = equity_value_exit;

            double irr_equity = calculate_irr(cf_equity);
            double irr_equity_percent = irr_equity * 100.0;

            // Store exit results
            exit_results[year] = {
                {"Exit Year", static_cast<double>(year)},
                {"Equity Value at Exit", equity_value_exit},
                {"Equity Investment", equity_investment},
                {"MoM", mom},
                {"IRR", irr_equity_percent},
                {"Enterprise Value at Exit", enterprise_value_exit},
                {"Net Debt at Exit", net_debt_exit}
            };
        }
    }

    return exit_results;
}
