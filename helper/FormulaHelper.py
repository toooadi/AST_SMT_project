import pysmt.fnode
import string
import random
from functools import reduce
from pysmt.typing import INT
from pysmt.shortcuts import LE, GE, And, Or, Int, Symbol
from pysmt.operators import IRA_RELATIONS

def generate_free_unused(f: pysmt.fnode) -> str:
    quantVars = get_quant_vars(f)
    usedVars = set([str(s) for s in f.get_free_variables()] + quantVars)
    newVar = random.choice(string.ascii_letters)
    while newVar in usedVars:
        newVar += random.choice(string.ascii_letters)

    return newVar

def get_quant_vars(f: pysmt.fnode) -> list[str]:
    if len(f.args()) == 0:
        return []
    quants = [str(s) for s in f.quantifier_vars()] if f.is_quantifier() else []
    
    return quants + reduce(lambda a, b: a + get_quant_vars(b), f.args(), [])

"""
generates a formula using the free variables in the already given formula
"""
def generate_int_formula(givenFormula: pysmt.fnode) -> pysmt.fnode:
    free_vars = [str(s) for s in givenFormula.get_free_variables()]
    new_vars = set()
    if len(free_vars) < 2:
        #only in this case utilize unused variables
        while len(new_vars) < 2:
            new_vars.add(generate_free_unused(givenFormula))
    else:
        while len(new_vars) < 2:
            new_vars.add(random.choice(free_vars))
        
        
    new_vars = list(new_vars)
    return Or(And(LE(Symbol(new_vars[0], INT), Int(0)), GE(Symbol(new_vars[1], INT), Int(3))), GE(Symbol(new_vars[0], INT), Int(5)))

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