// repayment_schedule.hpp

#pragma once

#include <string>
#include <map>

struct RepaymentSchedule {
    std::map<int, double> senior_a_repayments;
    std::map<int, double> senior_b_repayments;
    std::map<int, double> subordinate_repayments;
    std::map<int, double> mezzanine_repayments;
    std::map<int, double> rcf_utilization;
    std::map<int, double> rcf_repayments;
};
