from pysmt.fnode import FNode
from transformations.NonTrivialTransformation import NonTrivialTransformation
import random
from pysmt.typing import INT
from pysmt.shortcuts import Not, And, Equals, Int, Real

class WeakenNotEquals(NonTrivialTransformation):

    #pysmt doesn't actually have a NEQ operator
    def is_directly_applicable(self, f: FNode) -> bool:
        return f.is_not() and f.arg(0).is_equals()
    
    def apply(self, f: FNode) -> FNode:
        if (not self.is_directly_applicable(f)):
            raise RuntimeError("Transformation is not directly applicable to f.")
        
        left = f.arg(0).arg(0)
        right = f.arg(0).arg(1)
        equal_number = Int(random.randint(-50, 50)) if left.get_type() == INT else Real(random.random() * 100)
        return Not(And(Equals(left, equal_number), Equals(right, equal_number)))