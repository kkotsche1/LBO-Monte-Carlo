// case_data.hpp

#pragma once

#include <map>
#include <string>

struct CaseData {
    std::string name;
    // Key P&L Drivers
    std::map<int, double> revenue;
    std::map<int, double> ebitda;
    std::map<int, double> ebitda_normalizations;
    std::map<int, double> depreciation;
    std::map<int, double> amortization;
    std::map<int, double> ebit;
    // CapEx
    std::map<int, double> maintenance_capex;
    std::map<int, double> expansion_capex;
    // Balance Sheet Items
    std::map<int, double> inventory;
    std::map<int, double> accounts_receivable;
    std::map<int, double> accounts_payable;
    std::map<int, double> other_wc_assets;
    std::map<int, double> other_wc_liabilities;
    std::map<int, double> provisions;
    // Key Stats
    std::map<int, double> revenue_growth;
    std::map<int, double> ebitda_margin;
    std::map<int, double> depreciation_percent;
    std::map<int, double> amortization_percent;
    std::map<int, double> ebit_margin;
    std::map<int, double> m_capex_percent;
    std::map<int, double> e_capex_percent;
    std::map<int, double> inventory_percent;
    std::map<int, double> accounts_receivable_percent;
    std::map<int, double> accounts_payable_percent;
    std::map<int, double> other_wc_assets_percent;
    std::map<int, double> other_wc_liabilities_percent;
    std::map<int, double> provisions_growth;
};
