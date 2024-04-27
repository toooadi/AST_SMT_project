import pysmt.fnode

class Transformation:
    """
    Interface for formula transformations
    """

    """
    is_applicable(f): Tells us whether the transformation can be
        applied to formula f
    """

    def is_applicable(self, f: pysmt.fnode) -> bool:
        pass

    """
    apply(f): Perform the transformation on formula f
    """

    def apply(self, f: pysmt.fnode) -> pysmt.fnode:
        pass

    """
    apply(f, g): Perform generating transformation on formula f with input formula g that is added to the formula.
        Applied for transformations like Absorption
    """
    def apply(self, f: pysmt.fnode, g: pysmt.fnode) -> pysmt.fnode:
        pass