from Transformation import Transformation

class NonTrivialTransformation(Transformation):

    """
    Superclass for transformations which aren't always applicable but have to check the formula recursively

    This means that is_applicable remains the same, but is_directly_applicable has to be rewritten
    """

    def is_applicable(self, f):
        if (self.is_directly_applicable(f)):
            return True
        
        if (len(f.args()) > 0):
            return any(self.is_applicable(g) for g in f.args())
            
        
        return False