from NonTrivialTransformation import NonTrivialTransformation
from pysmt.shortcuts import Exists, Or

class ExistsSplit(NonTrivialTransformation):

    def is_directly_applicable(self, f):
        return f.is_exists() and len(f.args()) == 1 and f.arg(0).is_or()
    
    def apply(self, f):
        if (not self.is_directly_applicable(f)):
            raise RuntimeError("Transformation is not directly applicable to f.")
        
        quant_vars = f.quantifier_vars()
        return Or(Exists([v for v in quant_vars], g) for g in f.arg(0).args())