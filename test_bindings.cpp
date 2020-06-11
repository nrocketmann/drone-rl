//
// Created by Nameer Hirschkind on 5/20/20.
//
#include "pybind11/pybind11.h"
#include "pybind11/eigen.h"
namespace py = pybind11;

class Floof {
private:
    int number;
public:
    Floof(int num): number(num) {}
    int getnum() {return number;}
};

PYBIND11_MODULE(test, m) {
    py::class_<Floof>(m, "test")
            .def(py::init<int>())
            .def("update", &Floof::getnum);
}