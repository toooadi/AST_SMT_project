import pysmt.fnode
import AvailableTransformations as allTf
from Substituter import FirstOccurenceSubstituter

from pysmt.shortcuts import And, Or, Symbol

class EquivalentTransformer:
    substituter = FirstOccurenceSubstituter(None)

    """
    main class to fetch the formulas and perform equivalence transformations on them
    """

    def __init__(self) -> None:
        pass

    def get_applicable_transformations(self, formula):
        return [i for i in allTf.ALL if allTf.all_dict[i].is_applicable(formula)]
    
    #TODO: (1) We should define some heuristics for the transformation, so that it's not always the  most trivial transformations
    #          that get executed. One idea is to define some kind of ranking of the transformations, so that the simple ones are
    #          only executed if there is no other option
    #      (2) Implement functionality so that the substituter doesn't always go for the first possible match, but maybe the second
    #          or third one. This is especially important for the trivial transformations (which can always be executed) as they
    #          would always be executed top-level otherwise. Idea for this: Keep track of the tree depth and only transform on 
    #          level >=limit OR on the deepest level <limit which is transformable but doesn't have any transformable children
    def transform(self, formula, transformationId=None, generating_formula=None): #last two can be set for testing purposes
        applicable = self.get_applicable_transformations(formula)
        self.substituter.set_transformation(allTf.all_dict[transformationId])
        return self.substituter.substitute(formula, generating_formula)