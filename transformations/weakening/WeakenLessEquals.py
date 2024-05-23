

import random
from pysmt.fnode import FNode
from transformations.NonTrivialTransformation import NonTrivialTransformation
from pysmt.shortcuts import LT, Plus, Int, Real
from pysmt.typing import INT


class WeakenLessEquals(NonTrivialTransformation):

    def is_directly_applicable(self, f: FNode) -> bool:
        return f.is_le()
    
    def apply(self, f: FNode) -> FNode:
        if (not self.is_directly_applicable(f)):
            raise RuntimeError("Transformation is not directly applicable to f.")
        
        equal_number = Int(random.randint(1, 100)) if f.arg(1).get_type() == INT else Real(random.random() * 100 + 1)

        return LT(f.arg(0), Plus(f.arg(1), equal_number))