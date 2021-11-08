/*************************************************************************************************
GBDHash -- Copyright (c) 2020, Markus Iser, KIT - Karlsruhe Institute of Technology

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT
OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 **************************************************************************************************/

#include "Python.h"

#include "src/util/GBDHash.h"
#include "src/util/CNFFormula.h"
#include "src/util/ResourceLimits.h"

#include "src/features/CNFStats.h"
#include "src/features/GateStats.h"

static PyObject* version(PyObject* self) {
    return Py_BuildValue("i", 1);
}

static PyObject* gbdhash(PyObject* self, PyObject* arg) {
    const char* filename;

    if (!PyArg_ParseTuple(arg, "s", &filename)) {
        return nullptr;
    }

    std::string result = gbd_hash_from_dimacs(filename);

    return Py_BuildValue("s", result.c_str());
}

static PyObject* extract_base_features(PyObject* self, PyObject* arg) {
    const char* filename;
    unsigned rlim = 0, mlim = 0;

    if (!PyArg_ParseTuple(arg, "s|II", &filename, &rlim, &mlim)) {
        return nullptr;
    }

    PyObject *dict = PyDict_New();
    if (!dict) return nullptr;

    CNFFormula formula;
    formula.readDimacsFromFile(filename);
    ResourceLimits limits(rlim, mlim);

    CNFStats stats(formula, limits);
    try {
        limits.within_limits_or_throw();
        stats.analyze();
    } catch (ResourceLimitsExceeded& e) {
        PyObject *key = Py_BuildValue("s", "base_features_runtime");
        PyObject *val = Py_BuildValue("s", limits.within_memory_limit() ?  "timeout" : "memout");
        PyDict_SetItem(dict, key, val);
        return dict;
    } catch (std::bad_alloc& e) {
        return dict;
    }

    std::vector<float> record = stats.BaseFeatures();
    std::vector<std::string> names = CNFStats::BaseFeatureNames();

    for (unsigned int i = 0; i < record.size(); i++) {
        PyObject *key = Py_BuildValue("s", names[i].c_str());
        PyObject *num = PyFloat_FromDouble(static_cast<double>(record[i]));
        if (!num) {
            Py_DECREF(dict);
            return nullptr;
        }
        PyDict_SetItem(dict, key, num);
    }
    return dict;
}

static PyObject* extract_gate_features(PyObject* self, PyObject* arg) {
    const char* filename;
    unsigned rlim = 0, mlim = 0;

    if (!PyArg_ParseTuple(arg, "s|II", &filename, &rlim, &mlim)) {
        return nullptr;
    }

    PyObject *dict = PyDict_New();
    if (!dict) return nullptr;

    CNFFormula formula;
    formula.readDimacsFromFile(filename);
    ResourceLimits limits(rlim, mlim);

    GateStats stats(formula, limits);
    try {
        limits.within_limits_or_throw();
        stats.analyze(1, 0);
    } catch (ResourceLimitsExceeded& e) {
        PyObject *key = Py_BuildValue("s", "gate_features_runtime");
        PyObject *val = Py_BuildValue("s", limits.within_memory_limit() ?  "timeout" : "memout");
        PyDict_SetItem(dict, key, val);
        return dict;
    } catch (std::bad_alloc& e) {
        return dict;
    }

    std::vector<float> record = stats.GateFeatures();
    std::vector<std::string> names = GateStats::GateFeatureNames();

    for (unsigned int i = 0; i < record.size(); i++) {
        PyObject *key = Py_BuildValue("s", names[i].c_str());
        PyObject *num = PyFloat_FromDouble(static_cast<double>(record[i]));
        if (!num) {
            Py_DECREF(dict);
            return nullptr;
        }
        PyDict_SetItem(dict, key, num);
    }
    return dict;
}

static PyMethodDef myMethods[] = {
    {"extract_gate_features", extract_gate_features, METH_VARARGS, "Extract Gate Features."},
    {"extract_base_features", extract_base_features, METH_VARARGS, "Extract Base Features."},
    {"gbdhash", gbdhash, METH_VARARGS, "Calculates GBD-Hash of given DIMACS CNF file."},
    {"version", (PyCFunction)version, METH_NOARGS, "Returns Version"},
    {nullptr, nullptr, 0, nullptr}
};

static struct PyModuleDef myModule = {
    PyModuleDef_HEAD_INIT,
    "gbdc",
    "GBDC Accelerator Module",
    -1,
    myMethods
};

PyMODINIT_FUNC PyInit_gbdc(void) {
    return PyModule_Create(&myModule);
}
