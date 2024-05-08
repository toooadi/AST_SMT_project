import pysmt.fnode
import AvailableTransformations as allTf
from Substituter import FirstOccurenceSubstituter, NDepthSubstituter

from pysmt.shortcuts import And, Or, Symbol

class EquivalentTransformer:
    

    """
    main class to fetch the formulas and perform equivalence transformations on them
    """

    def __init__(self, subDepth=None) -> None:
        if (subDepth):
            self.substituter = NDepthSubstituter(None, subDepth)
        else:
            self.substituter = FirstOccurenceSubstituter(None)

    def get_applicable_transformations(self, formula):
        return [i for i in allTf.ALL if allTf.all_dict[i].is_applicable(formula)]
    
    #TODO: (1) We should define some heuristics for the transformation, so that it's not always the  most trivial transformations
    #          that get executed. One idea is to define some kind of ranking of the transformations, so that the simple ones are
    #          only executed if there is no other option
    def transform(self, formula, transformationId=None, generating_formula=None): #last two can be set for testing purposes
        applicable = self.get_applicable_transformations(formula)
        self.substituter.set_transformation(allTf.all_dict[transformationId])
        return self.substituter.substitute(formula, generating_formula)
    
def main():
    #TODO: Implement fetching of formulas from SMT-LIB suite, transformation etc. Implement with parameters like #transformations etc.
    pass

if __name__ == "__main__":
    main()