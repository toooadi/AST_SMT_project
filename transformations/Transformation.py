import pysmt.fnode

class Transformation:
    """
    Interface for formula transformations
    """

    """
    is_applicable(f): Tells us whether the transformation can be
        applied to formula f directly or any of its subformulae
    """

    def is_applicable(self, f: pysmt.fnode) -> bool:
        pass


    """
    is_directly_applicable(f): Tells us whether the transformation can be
        applied to formula f directly
    """

    def is_directly_applicable(self, f: pysmt.fnode) -> bool:
        pass

    """
    apply(f): Perform the transformation on formula f
        The transformation is performed directly on f, so if it is applicable to a subformula of f
        rather than f itself, the method will throw an error.
    """

    def apply(self, f: pysmt.fnode) -> pysmt.fnode:
        pass

    """
    apply(f, g): Perform generating transformation on formula f with input formula g that is added to the formula.
        Applied for transformations like Absorption
        The transformation is performed directly on f, so if it is applicable to a subformula of f
        rather than f itself, the method will throw an error.
    """
    def apply(self, f: pysmt.fnode, g: pysmt.fnode) -> pysmt.fnode:
        pass