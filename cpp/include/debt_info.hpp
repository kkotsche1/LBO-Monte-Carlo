// debt_info.hpp

#pragma once

#include <map>
#include <string>

struct DebtYearInfo {
    double opening_balance;
    double repayment;
    double closing_balance;
    double average_balance;
    double interest_rate;
    double interest_payment;

    // For RCF (Revolving Credit Facility)
    double rcf_utilization = 0.0;
    double rcf_repayment = 0.0;
    double commitment_fee = 0.0;
    double drawn_interest_fee = 0.0;
    double total_interest_payment = 0.0;
};

using DebtInfo = std::map<std::string, std::map<int, DebtYearInfo>>;
