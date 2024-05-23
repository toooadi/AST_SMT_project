from transformations.NonTrivialTransformation import NonTrivialTransformation
from pysmt.shortcuts import And, Or
from random import choice

class DistrOr(NonTrivialTransformation):

    def is_directly_applicable(self, f):
        return f.is_or() and len(f.args()) > 1 and any(g.is_and() for g in f.args())
    
    def apply(self, f):
        if (not self.is_directly_applicable(f)):
            raise RuntimeError("Transformation is not directly applicable to f.")
        
        andTerm = next(x for x in f.args() if x.is_and())
        rest = list(f.args())
        rest.remove(andTerm)
        joinTerm = choice(rest)
        rest.remove(joinTerm)
        distributed = And(Or(joinTerm, g) for g in andTerm.args())
        return Or([distributed] + rest) if len(rest) > 0 else distributed