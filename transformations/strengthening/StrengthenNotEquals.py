import random
from pysmt.fnode import FNode
from pysmt.shortcuts import LT, GT

from transformations.NonTrivialTransformation import NonTrivialTransformation

class StrengthenNotEquals(NonTrivialTransformation):
    def is_directly_applicable(self, f: FNode) -> bool:
        return f.is_not() and f.arg(0).is_equals()
    
    def apply(self, f: FNode) -> FNode:
        if (not self.is_directly_applicable(f)):
            raise RuntimeError("Transformation is not directly applicable to f.")
        
        left = f.arg(0).arg(0)
        right = f.arg(0).arg(1)

        return GT(left, right) if random.random() < 0.5 else LT(left, right)