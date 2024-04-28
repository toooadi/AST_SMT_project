import pysmt.fnode
import string
import random
from functools import reduce

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