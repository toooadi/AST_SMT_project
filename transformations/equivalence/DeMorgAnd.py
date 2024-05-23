from transformations.NonTrivialTransformation import NonTrivialTransformation
from pysmt.shortcuts import Or, Not

class DeMorgAnd(NonTrivialTransformation):
    
    def is_directly_applicable(self, f):
        return f.is_not() and len(f.args()) == 1 and f.args()[0].is_and()
    
    def apply(self, f):
        if (not self.is_directly_applicable(f)):
            raise RuntimeError("Transformation is not directly applicable to f.")
        
        return Or(Not(g) for g in f.args()[0].args())
