// bindings.cpp

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "lbo_model.hpp"

namespace py = pybind11;

PYBIND11_MODULE(lbo_cpp, m) {
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
