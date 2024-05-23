import random
from pysmt.fnode import FNode
from pysmt.shortcuts import And, LE, Int, Real
from pysmt.typing import INT

from transformations.NonTrivialTransformation import NonTrivialTransformation

class StrengthenEquals(NonTrivialTransformation):
    def is_directly_applicable(self, f: FNode) -> bool:
        return f.is_equals()
    
    def apply(self, f: FNode) -> FNode:
        if (not self.is_directly_applicable(f)):
            raise RuntimeError("Transformation is not directly applicable to f.")
        
        left = f.arg(0)
        right = f.arg(1)
        equal_number = Int(random.randint(-50, 50)) if left.get_type() == INT else Real(random.random() * 100)
        return And(LE(equal_number, left), LE(left, equal_number), LE(equal_number, right), LE(right, equal_number))
