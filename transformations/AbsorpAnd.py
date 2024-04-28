import Transformation
from pysmt.shortcuts import And, Or

class AbsorpAnd(Transformation):

    def is_applicable(self, f):
        return True
    
    def apply(self, f, g):
        return And(f, Or(f, g))