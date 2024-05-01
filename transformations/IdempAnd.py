from transformations.Transformation import Transformation
from pysmt.shortcuts import And

class IdempAnd(Transformation):

    def is_applicable(self, f):
        return True
    
    def apply(self, f):
        return And(f, f)