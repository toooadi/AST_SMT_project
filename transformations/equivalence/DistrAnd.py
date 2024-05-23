from transformations.NonTrivialTransformation import NonTrivialTransformation
from pysmt.shortcuts import And, Or
from random import choice

class DistrAnd(NonTrivialTransformation):

    def is_directly_applicable(self, f):
        return f.is_and() and len(f.args()) > 1 and any(g.is_or() for g in f.args())
    
    def apply(self, f):
        if (not self.is_directly_applicable(f)):
            raise RuntimeError("Transformation is not directly applicable to f.")
        
        orTerm = next(x for x in f.args() if x.is_or())
        rest = list(f.args())
        rest.remove(orTerm)
        joinTerm = choice(rest)
        rest.remove(joinTerm)
        distributed = Or(And(joinTerm, g) for g in orTerm.args())
        return And([distributed] + rest) if len(rest) > 0 else distributed
