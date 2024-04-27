import Transformation
from pysmt.shortcuts import Or

class IdempAnd(Transformation):

    def is_applicable(self, f):
        return True
    
    def apply(self, f):
        return Or(f, f)