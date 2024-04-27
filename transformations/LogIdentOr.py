import Transformation
from pysmt.shortcuts import And, Or, Not, Symbol
from helper.FormulaHelper import generate_free_unused
from pysmt.typing import INT

class LogIdentOr(Transformation):
    #The unsatisfiability here will be substituted by formula g which is of the form (X AND NOT(X))

    def is_applicable(self, f):
        return True
    
    def apply(self, f):
        newSymb = generate_free_unused(f)
        return Or(f, And(Symbol(newSymb, INT), Not(Symbol(newSymb, INT))))
    