from transformations.Transformation import Transformation
from pysmt.shortcuts import Not

class DoubleNeg(Transformation):

    def is_applicable(self, f) -> bool:
        return True
    
    def apply(self, f):
        return Not(Not(f))
    
