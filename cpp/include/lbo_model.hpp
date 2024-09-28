// lbo_model.hpp

#pragma once

#include <string>
#include <map>
#include <vector>

#include "case_data.hpp"
#include "deal_metrics.hpp"
#include "repayment_schedule.hpp"
#include "debt_info.hpp"

// Function declaration
std::map<int, std::map<std::string, double>> run_lbo_model_with_repayment_schedule(
    const DealMetrics& expanded_metrics,
    const CaseData& case_data,
    const RepaymentSchedule& repayment_schedule,
    const std::vector<int>& years,
    double tax_rate = 0.217,
    const std::vector<int>& exit_horizons = {2026, 2027, 2028, 2029}
);
