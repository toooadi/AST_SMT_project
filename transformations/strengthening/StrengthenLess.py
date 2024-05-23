import random
from pysmt.fnode import FNode
from pysmt.shortcuts import LE, Int, Real, Plus
from pysmt.typing import INT

from transformations.NonTrivialTransformation import NonTrivialTransformation

class StrengthenLess(NonTrivialTransformation):
    def is_directly_applicable(self, f: FNode) -> bool:
        return f.is_lt()
    
    def apply(self, f: FNode) -> FNode:
        if (not self.is_directly_applicable(f)):
            raise RuntimeError("Transformation is not directly applicable to f.")
        
        added_number = Int(random.randint(1, 100)) if f.arg(0).get_type() == INT else Real(random.random() * 100 + 1)

        return LE(Plus(f.arg(0), added_number), f.arg(0))