from NonTrivialTransformation import NonTrivialTransformation
from pysmt.shortcuts import  ForAll, Not

class ExistsNot(NonTrivialTransformation):

    def is_directly_applicable(self, f):
        return f.is_exists() and len(f.args()) == 1 and f.arg(0).is_not()
    
    def apply(self, f):
        if (not self.is_directly_applicable(f)):
            raise RuntimeError("Transformation is not directly applicable to f.")

        quant_vars = f.quantifier_vars()
        return Not(ForAll([v for v in quant_vars],f.arg(0).arg(0)))