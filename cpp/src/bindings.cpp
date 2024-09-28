// bindings.cpp

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "lbo_model.hpp"
#include "case_data.hpp"
#include "deal_metrics.hpp"
#include "repayment_schedule.hpp"
#include "debt_info.hpp"

namespace py = pybind11;

PYBIND11_MODULE(lbo_cpp, m) {
    // Bind CaseData
    py::class_<CaseData>(m, "CaseData")
        .def(py::init<>())
        .def_readwrite("name", &CaseData::name)
        .def_readwrite("revenue", &CaseData::revenue)
        .def_readwrite("ebitda", &CaseData::ebitda)
        .def_readwrite("ebitda_normalizations", &CaseData::ebitda_normalizations)
        .def_readwrite("depreciation", &CaseData::depreciation)
        .def_readwrite("amortization", &CaseData::amortization)
        .def_readwrite("ebit", &CaseData::ebit)
        .def_readwrite("maintenance_capex", &CaseData::maintenance_capex)
        .def_readwrite("expansion_capex", &CaseData::expansion_capex)
        .def_readwrite("inventory", &CaseData::inventory)
        .def_readwrite("accounts_receivable", &CaseData::accounts_receivable)
        .def_readwrite("accounts_payable", &CaseData::accounts_payable)
        .def_readwrite("other_wc_assets", &CaseData::other_wc_assets)
        .def_readwrite("other_wc_liabilities", &CaseData::other_wc_liabilities)
        .def_readwrite("provisions", &CaseData::provisions)
        .def_readwrite("revenue_growth", &CaseData::revenue_growth)
        .def_readwrite("ebitda_margin", &CaseData::ebitda_margin)
        .def_readwrite("depreciation_percent", &CaseData::depreciation_percent)
        .def_readwrite("amortization_percent", &CaseData::amortization_percent)
        .def_readwrite("ebit_margin", &CaseData::ebit_margin)
        .def_readwrite("m_capex_percent", &CaseData::m_capex_percent)
        .def_readwrite("e_capex_percent", &CaseData::e_capex_percent)
        .def_readwrite("inventory_percent", &CaseData::inventory_percent)
        .def_readwrite("accounts_receivable_percent", &CaseData::accounts_receivable_percent)
        .def_readwrite("accounts_payable_percent", &CaseData::accounts_payable_percent)
        .def_readwrite("other_wc_assets_percent", &CaseData::other_wc_assets_percent)
        .def_readwrite("other_wc_liabilities_percent", &CaseData::other_wc_liabilities_percent)
        .def_readwrite("provisions_growth", &CaseData::provisions_growth);

    // Bind ExitMetrics
    py::class_<ExitMetrics>(m, "ExitMetrics")
        .def(py::init<>())
        .def_readwrite("exit_multiple", &ExitMetrics::exit_multiple)
        .def_readwrite("enterprise_value_exit", &ExitMetrics::enterprise_value_exit)
        .def_readwrite("net_debt_exit", &ExitMetrics::net_debt_exit)
        .def_readwrite("equity_value_exit", &ExitMetrics::equity_value_exit)
        .def_readwrite("mom", &ExitMetrics::mom)
        .def_readwrite("irr", &ExitMetrics::irr);

    // Bind DealMetrics
    py::class_<DealMetrics>(m, "DealMetrics")
        .def(py::init<>())
        .def_readwrite("senior_a_amount", &DealMetrics::senior_a_amount)
        .def_readwrite("senior_a_interest", &DealMetrics::senior_a_interest)
        .def_readwrite("senior_b_amount", &DealMetrics::senior_b_amount)
        .def_readwrite("senior_b_interest", &DealMetrics::senior_b_interest)
        .def_readwrite("subordinate_amount", &DealMetrics::subordinate_amount)
        .def_readwrite("subordinate_interest", &DealMetrics::subordinate_interest)
        .def_readwrite("mezzanine_cash_amount", &DealMetrics::mezzanine_cash_amount)
        .def_readwrite("mezzanine_cash_interest", &DealMetrics::mezzanine_cash_interest)
        .def_readwrite("rcf_amount", &DealMetrics::rcf_amount)
        .def_readwrite("rcf_interest", &DealMetrics::rcf_interest)
        .def_readwrite("rcf_undrawn_interest", &DealMetrics::rcf_undrawn_interest)
        .def_readwrite("zqwl_equity", &DealMetrics::zqwl_equity)
        .def_readwrite("co_invest", &DealMetrics::co_invest)
        .def_readwrite("mpp", &DealMetrics::mpp)
        .def_readwrite("net_debt_at_closing", &DealMetrics::net_debt_at_closing)
        .def_readwrite("restricted_cash_and_overfunding", &DealMetrics::restricted_cash_and_overfunding)
        .def_readwrite("entry_multiple", &DealMetrics::entry_multiple)
        .def_readwrite("enterprise_value_entry", &DealMetrics::enterprise_value_entry)
        .def_readwrite("exit_metrics_by_period", &DealMetrics::exit_metrics_by_period);

    // Bind RepaymentSchedule
    py::class_<RepaymentSchedule>(m, "RepaymentSchedule")
        .def(py::init<>())
        .def_readwrite("senior_a_repayments", &RepaymentSchedule::senior_a_repayments)
        .def_readwrite("senior_b_repayments", &RepaymentSchedule::senior_b_repayments)
        .def_readwrite("subordinate_repayments", &RepaymentSchedule::subordinate_repayments)
        .def_readwrite("mezzanine_repayments", &RepaymentSchedule::mezzanine_repayments)
        .def_readwrite("rcf_utilization", &RepaymentSchedule::rcf_utilization)
        .def_readwrite("rcf_repayments", &RepaymentSchedule::rcf_repayments);

    // Bind DebtYearInfo
    py::class_<DebtYearInfo>(m, "DebtYearInfo")
        .def(py::init<>())
        .def_readwrite("opening_balance", &DebtYearInfo::opening_balance)
        .def_readwrite("repayment", &DebtYearInfo::repayment)
        .def_readwrite("closing_balance", &DebtYearInfo::closing_balance)
        .def_readwrite("average_balance", &DebtYearInfo::average_balance)
        .def_readwrite("interest_rate", &DebtYearInfo::interest_rate)
        .def_readwrite("interest_payment", &DebtYearInfo::interest_payment)
        .def_readwrite("rcf_utilization", &DebtYearInfo::rcf_utilization)
        .def_readwrite("rcf_repayment", &DebtYearInfo::rcf_repayment)
        .def_readwrite("commitment_fee", &DebtYearInfo::commitment_fee)
        .def_readwrite("drawn_interest_fee", &DebtYearInfo::drawn_interest_fee)
        .def_readwrite("total_interest_payment", &DebtYearInfo::total_interest_payment);

    // Bind DebtInfo (Note: pybind11 supports automatic conversion of std::map)
    // So you can return DebtInfo directly to Python

    // Bind the run_lbo_model_with_repayment_schedule function
    m.def("run_lbo_model_with_repayment_schedule", &run_lbo_model_with_repayment_schedule,
          "Run the LBO model with repayment schedule",
          py::arg("expanded_metrics"),
          py::arg("case_data"),
          py::arg("repayment_schedule"),
          py::arg("years"),
          py::arg("tax_rate") = 0.217,
          py::arg("exit_horizons") = std::vector<int>{2026, 2027, 2028, 2029});
}
