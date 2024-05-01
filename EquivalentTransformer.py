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
    
    def transform(self, formula):
        applicable = self.get_applicable_transformations(formula)
        self.substituter.set_transformation(allTf.all_dict[allTf.DISTR_AND])
        return self.substituter.substitute(formula)
    
frml = And(Symbol("A"), Or(Symbol("B"), Symbol("C")))
transformer = EquivalentTransformer()
print(transformer.transform(frml))