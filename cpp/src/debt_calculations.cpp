// debt_calculations.cpp

#include "debt_calculations.hpp"
#include <algorithm>
#include <numeric>
#include <iostream>

DebtInfo calculate_debt_balances_and_interest(
    const DealMetrics& deal_metrics,
    const RepaymentSchedule& repayment_schedule,
    const InterestRates& interest_rates,
    const std::map<std::string, double>& starting_balances,
    const std::vector<int>& years
) {
    DebtInfo debt_info;
    std::map<std::string, double> balances = starting_balances;

    for (int year : years) {
        // Handle Senior A, Senior B, Subordinate, and Mezzanine debt
        for (const std::string& debt_type : {"Senior A", "Senior B", "Subordinate", "Mezzanine"}) {
            double opening_balance = balances[debt_type];
            double repayment = 0.0;  // Default repayment to 0.0

            // Get repayment amount from repayment_schedule if it exists, otherwise default to 0.0
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

            double closing_balance = opening_balance - repayment;  // Repayments reduce the balance

            // Calculate interest
            double interest_payment = 0.0;
            double average_balance = (opening_balance + closing_balance) / 2.0;
            interest_payment = average_balance * interest_rates.at(debt_type);

            // Store values for this year
            DebtYearInfo year_info;
            year_info.opening_balance = opening_balance;
            year_info.repayment = repayment;
            year_info.closing_balance = closing_balance;
            year_info.average_balance = average_balance;
            year_info.interest_rate = interest_rates.at(debt_type);
            year_info.interest_payment = interest_payment;

            debt_info[debt_type][year] = year_info;

            // Update balance for next year
            balances[debt_type] = closing_balance;
        }

        // Handle RCF (Revolving Credit Facility)
        const std::string debt_type = "RCF";
        double opening_balance = balances[debt_type];
        double rcf_utilization = repayment_schedule.rcf_utilization.count(year) ? repayment_schedule.rcf_utilization.at(year) : 0.0;
        double rcf_repayment = repayment_schedule.rcf_repayments.count(year) ? repayment_schedule.rcf_repayments.at(year) : 0.0;
        double closing_balance = opening_balance + rcf_utilization - rcf_repayment;

        // Interest on the drawn amount
        double average_balance = (opening_balance + closing_balance) / 2.0;
        double interest_rate = interest_rates.at(debt_type);
        double drawn_interest_payment = average_balance * interest_rate;

        // Ensure undrawn balance interest is calculated and added properly
        double max_revolver_draw = deal_metrics.rcf_amount;
        double undrawn_balance = max_revolver_draw - closing_balance;
        double commitment_fee = undrawn_balance * deal_metrics.rcf_undrawn_interest;

        // Total interest payment is the sum of interest on the drawn amount and the undrawn commitment fee
        double total_interest_payment = drawn_interest_payment + commitment_fee;


        // Store values for this year
        DebtYearInfo year_info = {};
        year_info.opening_balance = opening_balance;
        year_info.rcf_utilization = rcf_utilization;
        year_info.rcf_repayment = rcf_repayment;
        year_info.closing_balance = closing_balance;
        year_info.average_balance = average_balance;
        year_info.interest_rate = interest_rate;
        year_info.drawn_interest_fee = drawn_interest_payment;
        year_info.commitment_fee = commitment_fee;
        year_info.total_interest_payment = total_interest_payment;

        debt_info[debt_type][year] = year_info;

        // Update balance for next year
        balances[debt_type] = closing_balance;
    }

    return debt_info;
}
