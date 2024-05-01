from transformations.Transformation import Transformation
from pysmt.shortcuts import And, Or, Not, Symbol
from helper.FormulaHelper import generate_free_unused
from pysmt.typing import INT

class LogIdentAnd(Transformation):
    #The tautology here will be substituted by formula g which is of the form (X OR Not(X))

    def is_applicable(self, f):
        return True
    
    def apply(self, f):
        newSymb = generate_free_unused(f)
        return And(f, Or(Symbol(newSymb, INT), Not(Symbol(newSymb, INT))))