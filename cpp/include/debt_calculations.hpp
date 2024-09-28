// debt_calculations.hpp

#pragma once

#include "deal_metrics.hpp"
#include "repayment_schedule.hpp"
#include "debt_info.hpp"
#include "interest_rates.hpp"
#include <vector>

DebtInfo calculate_debt_balances_and_interest(
    const DealMetrics& deal_metrics,
    const RepaymentSchedule& repayment_schedule,
    const InterestRates& interest_rates,
    const std::map<std::string, double>& starting_balances,
    const std::vector<int>& years
);
