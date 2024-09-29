#include <iostream>
#include "include/lbo_model.hpp"
#include "include/case_data.hpp"
#include "include/deal_metrics.hpp"
#include "include/repayment_schedule.hpp"
#include "include/debt_info.hpp"

CaseData get_sample_case_data() {
    CaseData case_data;
    case_data.name = "Primary Case";
    case_data.revenue = {{2023, 181.581}, {2024, 211.5}, {2025, 250.0}, {2026, 295.0}, {2027, 345.0}};
    case_data.ebitda = {{2023, 6.0571}, {2024, 10.3057}, {2025, 12.4436}, {2026, 14.5996}, {2027, 17.1087}};
    case_data.ebitda_normalizations = {{2023, 1.5}, {2024, 0.0}, {2025, 0.0}, {2026, 0.0}, {2027, 0.0}};
    case_data.depreciation = {{2023, -0.2624}, {2024, -0.21}, {2025, -0.26}, {2026, -0.29}, {2027, -0.32}};
    case_data.amortization = {{2023, 0.0}, {2024, 0.0}, {2025, 0.0}, {2026, 0.0}, {2027, 0.0}};
    case_data.ebit = {{2023, 5.7947}, {2024, 10.0957}, {2025, 12.1836}, {2026, 14.3096}, {2027, 16.7887}};
    case_data.maintenance_capex = {{2023, -1.1}, {2024, -1.2812}, {2025, -1.5144}, {2026, -1.7870}, {2027, -2.0899}};
    case_data.expansion_capex = {{2023, 0.0}, {2024, 0.0}, {2025, 0.0}, {2026, 0.0}, {2027, 0.0}};

    // Add m_capex_percent and e_capex_percent
    case_data.m_capex_percent = {{2023, 0.006}, {2024, 0.006}, {2025, 0.006}, {2026, 0.006}, {2027, 0.006}};  // 0.6% of revenue for maintenance CapEx
    case_data.e_capex_percent = {{2023, 0.003}, {2024, 0.003}, {2025, 0.003}, {2026, 0.003}, {2027, 0.003}};  // 0.3% of revenue for expansion CapEx

    // Add working capital percentages
    case_data.inventory_percent = {{2023, 0.117}, {2024, 0.117}, {2025, 0.117}, {2026, 0.117}, {2027, 0.117}};
    case_data.accounts_receivable_percent = {{2023, 0.074}, {2024, 0.074}, {2025, 0.074}, {2026, 0.074}, {2027, 0.074}};
    case_data.accounts_payable_percent = {{2023, 0.021}, {2024, 0.021}, {2025, 0.021}, {2026, 0.021}, {2027, 0.021}};
    case_data.other_wc_assets_percent = {{2023, 0.002}, {2024, 0.002}, {2025, 0.002}, {2026, 0.002}, {2027, 0.002}};
    case_data.other_wc_liabilities_percent = {{2023, 0.018}, {2024, 0.018}, {2025, 0.018}, {2026, 0.018}, {2027, 0.018}};

    case_data.inventory = {{2023, 21.3074}, {2024, 24.8182}, {2025, 29.3359}, {2026, 34.6164}, {2027, 40.4836}};
    case_data.accounts_receivable = {{2023, 13.3729}, {2024, 15.5763}, {2025, 18.4118}, {2026, 21.7259}, {2027, 25.4083}};
    case_data.accounts_payable = {{2023, -3.8253}, {2024, -4.4556}, {2025, -5.2667}, {2026, -6.2147}, {2027, -7.2680}};
    case_data.other_wc_assets = {{2023, 0.2806}, {2024, 105.75}, {2025, 125.0}, {2026, 147.5}, {2027, 172.5}};
    case_data.other_wc_liabilities = {{2023, -3.3489}, {2024, -3.9007}, {2025, -4.6107}, {2026, -5.4406}, {2027, -6.3628}};
    case_data.provisions = {{2023, 1.0}, {2024, 1.0}, {2025, 1.0}, {2026, 1.0}, {2027, 1.0}};
    case_data.ebitda_margin = {{2023, 0.0333}, {2024, 0.05}, {2025, 0.05}, {2026, 0.05}, {2027, 0.05}};
    case_data.depreciation_percent = {{2023, 0.0014}, {2024, 0.0014}, {2025, 0.0014}, {2026, 0.0014}, {2027, 0.0014}};
    case_data.amortization_percent = {{2023, 0.0}, {2024, 0.0}, {2025, 0.0}, {2026, 0.0}, {2027, 0.0}};

    return case_data;
}


DealMetrics get_sample_deal_metrics() {
    DealMetrics deal_metrics;
    deal_metrics.senior_a_amount = 11.33568;
    deal_metrics.senior_a_interest = 0.0375;
    deal_metrics.senior_b_amount = 11.33568;
    deal_metrics.senior_b_interest = 0.0425;
    deal_metrics.subordinate_amount = 0.0;
    deal_metrics.subordinate_interest = 0.0725;
    deal_metrics.mezzanine_cash_amount = 0.0;
    deal_metrics.mezzanine_cash_interest = 0.045;
    deal_metrics.rcf_amount = 5.0;
    deal_metrics.rcf_interest = 0.025;
    deal_metrics.rcf_undrawn_interest = 0.006;
    deal_metrics.zqwl_equity = 51.17655;
    deal_metrics.entry_multiple = 10.0;
    // Add exit multiples for different exit periods (e.g., after 3, 4, 5 years)
    deal_metrics.exit_metrics_by_period = {
        {"2026", {10.0, 295.0, -10.0, 285.0, 2.5, 0.15}}, // Example for 2026
        {"2027", {10.5, 345.0, -5.0, 340.0, 3.0, 0.18}},  // Example for 2027
        {"2028", {11.0, 395.0, 0.0, 395.0, 3.5, 0.20}},   // Example for 2028
    };

    return deal_metrics;
}

RepaymentSchedule get_sample_repayment_schedule() {
    RepaymentSchedule repayment_schedule;
    repayment_schedule.senior_a_repayments = {{2023, 0.0}, {2024, -1.133568}, {2025, -1.700352}, {2026, -1.700352}, {2027, -2.267136}};
    repayment_schedule.senior_b_repayments = {{2023, 0.0}, {2024, -1.133568}, {2025, -1.700352}, {2026, -1.700352}, {2027, -2.267136}};
    repayment_schedule.rcf_utilization = {{2023, 0.0}, {2024, 0.734167}, {2025, 1.667843}, {2026, 1.154949}};
    repayment_schedule.rcf_repayments = {{2023, 0.0}, {2024, 0.0}, {2025, 0.0}, {2026, 0.0}, {2027, 0.0}};
    return repayment_schedule;
}

int main() {
    // Sample years and exit horizons
    std::vector<int> years = {2023, 2024, 2025, 2026, 2027};
    std::vector<int> exit_horizons = {2026, 2027};

    // Tax rate
    double tax_rate = 0.217;

    // Get sample data
    CaseData case_data = get_sample_case_data();
    DealMetrics deal_metrics = get_sample_deal_metrics();
    RepaymentSchedule repayment_schedule = get_sample_repayment_schedule();

    // Run the LBO model
    std::map<int, std::map<std::string, double>> result = run_lbo_model_with_repayment_schedule(
        deal_metrics, case_data, repayment_schedule, years, tax_rate, exit_horizons
    );

    // Output the results
    for (const auto& [year, metrics] : result) {
        std::cout << "Year: " << year << std::endl;
        for (const auto& [key, value] : metrics) {
            std::cout << key << ": " << value << std::endl;  // Ensure key is a string and value is a number
        }
        std::cout << std::endl;
    }


    return 0;
}
