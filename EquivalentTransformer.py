import pysmt.fnode
import AvailableTransformations as allTransformations
import random
import os
from Substituter import FirstOccurenceSubstituter, NDepthSubstituter
from pysmt.smtlib.parser import SmtLibParser

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
        return [i for i in allTransformations.ALL if allTransformations.obj_dict[i].is_applicable(formula)]
    
    """
    We use weights for the transformation types so that non-trivial tranformations are favored when applicable
    """
    def transform(self, formula, transformationId=None, generating_formula=None): #last two can be set for testing purposes
        applicable = self.get_applicable_transformations(formula)
        if (not transformationId):
            transformationId = random.choices(applicable, weights=[allTransformations.weights[i] for i in applicable], k=1)
        self.substituter.set_transformation(allTransformations.obj_dict[transformationId])
        return self.substituter.substitute(formula, generating_formula)
    
def main():
    #TODO: Implement fetching of formulas from SMT-LIB suite, transformation etc. Implement with parameters like #transformations etc.
    parser = SmtLibParser()

    directory = "benchmarks/<ADD REST OF PATH>"
    for filename in os.listdir(directory):
        smtFile = open(os.path.join(directory, filename), "r")
        script = parser.get_script(smtFile)
        formula = script.get_last_formula()
        #do transformations & Solving

    #TESTING
    smtFile = open("./benchmarks/non-incremental/LIA/psyco/017.smt2", "r")
    script = parser.get_script(smtFile)
    #most smt-lib formulas of the benchmarks have a bunch of assert statements which are all AND-ed by this
    formula = script.get_last_formula()
    print(formula)



if __name__ == "__main__":
    main()