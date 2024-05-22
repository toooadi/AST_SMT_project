import pysmt.fnode
from helper.FormulaHelper import is_op_returns_bool

class Transformation:
    """
    Interface for formula transformations
    """

    """
    is_applicable(f): Tells us whether the transformation can be
        applied to formula f directly or any of its subformulae
    """

    def is_applicable(self, f: pysmt.fnode.FNode) -> bool:
        pass


    """
    is_directly_applicable(f): Tells us whether the transformation can be
        applied to formula f directly. Trivially, since we are using boolean
        transformations, formula MUST be some kind of boolean operator (E.g. And, Or, LE, Eq)
    """

    def is_directly_applicable(self, f: pysmt.fnode.FNode) -> bool:
        return is_op_returns_bool(f)

    """
    apply(f): Perform the transformation on formula f
        The transformation is performed directly on f, so if it is applicable to a subformula of f
        rather than f itself, the method will throw an error.
    """

    def apply(self, f: pysmt.fnode.FNode) -> pysmt.fnode.FNode:
        pass

    """
    apply(f, g): Perform generating transformation on formula f with input formula g that is added to the formula.
        Applied for transformations like Absorption
        The transformation is performed directly on f, so if it is applicable to a subformula of f
        rather than f itself, the method will throw an error.
    """
    def apply(self, f: pysmt.fnode.FNode, g: pysmt.fnode.FNode) -> pysmt.fnode.FNode:
        pass

    def is_generating_transformation(self):
        return False