
import random
from pysmt.shortcuts import LE, NotEquals
from pysmt.fnode import FNode
from transformations.NonTrivialTransformation import NonTrivialTransformation


class WeakenLess(NonTrivialTransformation):
    def is_directly_applicable(self, f: FNode) -> bool:
        return f.is_lt()
    
    def apply(self, f: FNode) -> FNode:
        if (not self.is_directly_applicable(f)):
            raise RuntimeError("Transformation is not directly applicable to f.")
        
        left = f.arg(0)
        right = f.arg(1)

        return LE(left, right) if random.random() < 0.5 else NotEquals(left, right)