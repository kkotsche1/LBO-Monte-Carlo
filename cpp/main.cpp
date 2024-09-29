#include <iostream>
#include "include/lbo_model.hpp"
#include "include/case_data.hpp"
#include "include/deal_metrics.hpp"
#include "include/repayment_schedule.hpp"
#include "include/debt_info.hpp"

CaseData get_sample_case_data() {
    CaseData case_data;
    case_data.name = "Management Case";
    case_data.revenue = {
        {2023, 181.581}, {2024, 211.5}, {2025, 250.0}, {2026, 295.0},
        {2027, 345.0}, {2028, 396.75}, {2029, 456.2625}, {2030, 524.701875}
    };
    case_data.ebitda = {
        {2023, 6.0571}, {2024, 10.3058}, {2025, 12.4436}, {2026, 14.5996},
        {2027, 17.1087}, {2028, 39.675}, {2029, 45.62625}, {2030, 52.4701875}
    };
    case_data.ebitda_normalizations = {
        {2023, 1.5}, {2024, 0.0}, {2025, 0.0}, {2026, 0.0}, {2027, 0.0},
        {2028, 0.0}, {2029, 0.0}, {2030, 0.0}
    };
    case_data.depreciation = {
        {2023, -0.2624}, {2024, -0.21}, {2025, -0.26}, {2026, -0.29},
        {2027, -0.32}, {2028, -0.368}, {2029, -0.4232}, {2030, -0.48668}
    };
    case_data.amortization = {
        {2023, 0.0}, {2024, 0.0}, {2025, 0.0}, {2026, 0.0},
        {2027, 0.0}, {2028, 0.0}, {2029, 0.0}, {2030, 0.0}
    };
    case_data.ebit = {
        {2023, 5.7947}, {2024, 10.0958}, {2025, 12.1836}, {2026, 14.3096},
        {2027, 16.7887}, {2028, 39.307}, {2029, 45.20305}, {2030, 51.9835075}
    };
    case_data.maintenance_capex = {
        {2023, -1.1}, {2024, -1.2812}, {2025, -1.5144}, {2026, -1.7871},
        {2027, -2.08998}, {2028, -2.40347}, {2029, -2.76399}, {2030, -3.17859}
    };
    case_data.expansion_capex = {
        {2023, 0.0}, {2024, 0.0}, {2025, 0.0}, {2026, 0.0},
        {2027, 0.0}, {2028, 0.0}, {2029, 0.0}, {2030, 0.0}
    };

    // Working capital percentages
    case_data.inventory_percent = {
        {2023, 0.117}, {2024, 0.117}, {2025, 0.117}, {2026, 0.117},
        {2027, 0.117}, {2028, 0.117}, {2029, 0.117}, {2030, 0.117}
    };
    case_data.accounts_receivable_percent = {
        {2023, 0.0736}, {2024, 0.0736}, {2025, 0.0736}, {2026, 0.0736},
        {2027, 0.0736}, {2028, 0.0736}, {2029, 0.0736}, {2030, 0.0736}
    };
    case_data.accounts_payable_percent = {
        {2023, 0.021}, {2024, 0.021}, {2025, 0.021}, {2026, 0.021},
        {2027, 0.021}, {2028, 0.021}, {2029, 0.021}, {2030, 0.021}
    };
    case_data.other_wc_assets_percent = {
        {2023, 0.002}, {2024, 0.002}, {2025, 0.002}, {2026, 0.002},
        {2027, 0.002}, {2028, 0.002}, {2029, 0.002}, {2030, 0.002}
    };
    case_data.other_wc_liabilities_percent = {
        {2023, 0.018}, {2024, 0.018}, {2025, 0.018}, {2026, 0.018},
        {2027, 0.018}, {2028, 0.018}, {2029, 0.018}, {2030, 0.018}
    };

    case_data.provisions = {
        {2023, 1.0}, {2024, 1.0}, {2025, 1.0}, {2026, 1.0},
        {2027, 1.0}, {2028, 1.0}, {2029, 1.0}, {2030, 1.0}
    };
    case_data.ebitda_margin = {
        {2023, 0.0334}, {2024, 0.0487}, {2025, 0.0498}, {2026, 0.0495},
        {2027, 0.0496}, {2028, 0.1}, {2029, 0.1}, {2030, 0.1}
    };
    case_data.depreciation_percent = {
        {2023, 0.0014}, {2024, 0.001}, {2025, 0.001}, {2026, 0.001},
        {2027, 0.001}, {2028, 0.001}, {2029, 0.001}, {2030, 0.001}
    };
    case_data.amortization_percent = {
        {2023, 0.0}, {2024, 0.0}, {2025, 0.0}, {2026, 0.0},
        {2027, 0.0}, {2028, 0.0}, {2029, 0.0}, {2030, 0.0}
    };

    // Set m_capex_percent to 0.6% and e_capex_percent to 0% for all years
    case_data.m_capex_percent = {
        {2023, 0.006}, {2024, 0.006}, {2025, 0.006}, {2026, 0.006},
        {2027, 0.006}, {2028, 0.006}, {2029, 0.006}, {2030, 0.006}
    };
    case_data.e_capex_percent = {
        {2023, 0.0}, {2024, 0.0}, {2025, 0.0}, {2026, 0.0},
        {2027, 0.0}, {2028, 0.0}, {2029, 0.0}, {2030, 0.0}
    };

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
    deal_metrics.zqwl_equity = 51.1765536;
    deal_metrics.entry_multiple = 10.0;

    // Add exit metrics for each exit horizon
    deal_metrics.exit_metrics_by_period = {
        {"2026", {10.0, 145.996, -17.1597, 128.8366, 2.52, 58.76}},
        {"2027", {10.0, 171.0874, -13.9142, 157.1732, 3.07, 59.41}},
        {"2028", {10.0, 396.75, 6.5982, 403.3482, 7.88, 75.28}},
        {"2029", {10.0, 456.2625, 30.3956, 486.6581, 9.51, 64.71}}
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
    std::vector<int> years = {2024, 2025, 2026, 2027};
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
