import random
import string
import subprocess
import time
from functools import reduce

import cvc5
import pysmt.fnode
import z3
from pysmt.operators import IRA_RELATIONS
from pysmt.shortcuts import GE, LE, And, Int, Or, Real, Symbol
from pysmt.typing import BOOL, INT, REAL


def generate_free_unused(f: pysmt.fnode.FNode) -> str:
    quantVars = get_quant_vars(f)
    usedVars = set([str(s) for s in f.get_free_variables()] + quantVars)
    newVar = random.choice(string.ascii_letters)
    while newVar in usedVars:
        newVar += random.choice(string.ascii_letters)

    return newVar

def get_quant_vars(f: pysmt.fnode.FNode) -> list[str]:
    if len(f.args()) == 0:
        return []
    quants = [str(s) for s in f.quantifier_vars()] if f.is_quantifier() else []
    
    return quants + reduce(lambda a, b: a + get_quant_vars(b), f.args(), [])

"""
generates a formula using the free variables in the already given formula
"""
def generate_formula(givenFormula: pysmt.fnode.FNode) -> pysmt.fnode.FNode:
    int_vars = [s for s in givenFormula.get_free_variables() if s.get_type() == INT]
    real_vars = [s for s in givenFormula.get_free_variables() if s.get_type() == REAL]
    bool_vars = [s for s in givenFormula.get_free_variables() if s.get_type() == BOOL]
    if len(int_vars) < 2 and len(real_vars) < 2 and len(bool_vars) < 3:
        #only in this case utilize unused variables
        return Or(Symbol(generate_free_unused(givenFormula)), And(Symbol(generate_free_unused(givenFormula)), Symbol(generate_free_unused(givenFormula))))
    elif (len(real_vars) >= 2):
         new_vars = random.sample(real_vars, k=2)
         return Or(And(LE(new_vars[0], Real(0.0)), GE(new_vars[1], Real(3.0))), GE(new_vars[0], Real(5.0)))
    elif (len(int_vars) >= 2):
         new_vars = random.sample(int_vars, k=2)
         return Or(And(LE(new_vars[0], Int(0)), GE(new_vars[1], Int(3))), GE(new_vars[0], Int(5)))
    else:
         new_vars = random.sample(bool_vars, k=3)
         return Or(new_vars[0], And(new_vars[1], new_vars[2]))

def is_ira_relation(formula):
    return formula.node_type() in IRA_RELATIONS

def is_op_returns_bool(formula):
        return formula.is_bool_op() or is_ira_relation(formula) or formula.is_equals()

def find_maxDepth(formula, curr):
        if (is_op_returns_bool(formula)):
            curr += 1
            if (len(formula.args()) > 1):
                return max(find_maxDepth(f, curr) for f in formula.args())
        return curr

def solve_smt2_file(filePath, TIMEOUT, solver="z3"):
    if (solver == "z3"):
        return solve_smt2_file_z3(filePath, TIMEOUT)
    elif (solver == "cvc5"):
        res = solve_smt2_file_cvc5(filePath, TIMEOUT)
        return res
    else:
        return "Error", 0

def solve_smt2_file_z3(filePath, TIMEOUT):
    try:
        solver = z3.Solver()
        solver.add(z3.parse_smt2_file(filePath))
        solver.set("timeout", TIMEOUT)

        start_time = time.time()
        result = solver.check()
        end_time = time.time()

        result_string = "sat" if result == z3.sat else "unsat" if result == z3.unsat else "timeout" if solver.reason_unknown() == "timeout" else "unknown"
        return result_string, end_time - start_time
    except  Exception:
        return "Error", 0
    
def solve_smt2_file_cvc5(filePath, TIMEOUT=60000):
    try:
        start_time = time.time()
        
        result = subprocess.run(["cvc5", "--tlimit=" + str(TIMEOUT), filePath], stdout=subprocess.PIPE)
        end_time = time.time()

        return result.stdout.decode('utf-8').strip("\n"), end_time - start_time
    except Exception:
         return "Error", 0


