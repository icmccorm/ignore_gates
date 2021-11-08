/*************************************************************************************************
CNFTools -- Copyright (c) 2015, Markus Iser, KIT - Karlsruhe Institute of Technology

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

#ifndef SRC_GATES_OCCURRENCELIST_H_
#define SRC_GATES_OCCURRENCELIST_H_

#include <vector>
#include <set>
#include <limits>
#include <utility>

#include "src/util/CNFFormula.h"

class OccurrenceList {
    const CNFFormula& problem;

    std::vector<For> index;
    std::vector<Cl*> unitc;
    Lit max_literal;

#define CLAUSES_ARE_SORTED
#ifdef CLAUSES_ARE_SORTED
    bool isBlocked(Lit o, const Cl& c1, const Cl& c2) const {  // assert o \in c1 and ~o \in c2
        for (unsigned i = 0, j = 0; i < c1.size() && j < c2.size(); c1[i] < c2[j] ? ++i : ++j) {
            if (c1[i] != o && c1[i] == ~c2[j]) return true;
        }
        return false;
    }
#else
    bool isBlocked(Lit o, const Cl& c1, const Cl& c2) const {  // assert o \in c1 and ~o \in c2
        for (Lit l1 : c1) if (l1 != o) for (Lit l2 : c2) if (l1 == ~l2) return true;
        return false;
    }
#endif

 public:
    explicit OccurrenceList(const CNFFormula& problem_) : problem(problem_), unitc(), max_literal(problem.nVars(), true) {
        index.resize(2 + 2 * problem.nVars());

        for (Cl* clause : problem_) {
            if (clause->size() == 1) {
                unitc.push_back(clause);
            } else {
                for (Lit lit : *clause) {
                    index[lit].push_back(clause);
                }
            }
        }
    }

    ~OccurrenceList() { }

    void remove(const For& list) {
        for (Cl* clause : list) for (Lit lit : *clause) {
            if (!index[lit].empty()) {
                // assert(std::find(index[lit].begin(), index[lit].end(), clause) != index[lit].end());
                auto it = index[lit].begin();
                while (*it != clause && it != index[lit].end()) {
                    ++it;
                }
                while (it+1 < index[lit].end()) {
                    *it = *(it+1);
                    ++it;
                }
                index[lit].erase(index[lit].end()-1, index[lit].end());
            }
        }
    }

    inline const For& operator[] (size_t o) const {
        return index[o];
    }

    inline size_t size() const {
        return index.size();
    }

    inline bool isBlockedSet(Lit o) {
        for (Cl* c1 : index[o]) {
            for (Cl* c2 : index[~o]) {
                if (!isBlocked(o, *c1, *c2)) {
                    return false;
                }
            }
        }
        return true;
    }

    For estimateRoots() {
        For result {};

        if (unitc.size() > 0) {
            std::swap(result, unitc);
        } else {
            while (max_literal > 0 && index[max_literal].size() == 0) {
                --max_literal;
            }
            if (max_literal > 0) {
                result.swap(index[max_literal]);
                remove(result);
            }
        }

        return result;
    }
};

#endif  // SRC_GATES_OCCURRENCELIST_H_
