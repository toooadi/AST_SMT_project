import random
from pysmt.fnode import FNode
from pysmt.typing import INT
from pysmt.shortcuts import Equals, Plus, LT, Int, Real

from transformations.NonTrivialTransformation import NonTrivialTransformation

class StrengthenLessEquals(NonTrivialTransformation):
    def is_directly_applicable(self, f: FNode) -> bool:
        return f.is_le()
    
    def apply(self, f: FNode) -> FNode:
        if (not self.is_directly_applicable(f)):
            raise RuntimeError("Transformation is not directly applicable to f.")
        
        left = f.arg(0)
        right = f.arg(1)
        added_number = Int(random.randint(0, 100)) if left.get_type() == INT else Real(random.random() * 100)

        return Equals(left, right) if random.random() < 0.5 else LT(Plus(left, added_number), right)