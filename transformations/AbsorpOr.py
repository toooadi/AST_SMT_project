from Transformation import Transformation
from pysmt.shortcuts import And, Or

class AbsorpOr(Transformation):
    
    def is_applicable(self, f):
        return True
    
    def apply(self, f, g):
        return Or(f, And(f, g))