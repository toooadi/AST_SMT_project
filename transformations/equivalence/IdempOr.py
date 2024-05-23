from transformations.Transformation import Transformation
from pysmt.shortcuts import Or

class IdempOr(Transformation):

    def is_applicable(self, f):
        return True
    
    def apply(self, f):
        return Or(f, f)