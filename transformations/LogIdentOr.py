from transformations.Transformation import Transformation
from pysmt.shortcuts import And, Or, Not, Symbol
from helper.FormulaHelper import generate_free_unused
from pysmt.typing import INT

class LogIdentOr(Transformation):
    #The unsatisfiability here will be substituted by formula g which is of the form (X AND NOT(X))

    def is_applicable(self, f):
        return True
    
    def is_generating_transformation(self):
        return True
    
    def apply(self, f, g):
        return Or(f, And(g, Not(g)))
    