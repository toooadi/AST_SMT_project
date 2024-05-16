import pysmt.fnode
import AvailableTransformations as allTransformations
import random
import os
from Substituter import FirstOccurenceSubstituter, NDepthSubstituter
from pysmt.smtlib.parser import SmtLibParser
import pysmt.smtlib.commands as commands
from pysmt.logics import QF_LIA, QF_LRA, QF_NIA, LIA
import subprocess
import shutil
import sys
from helper.FormulaHelper import generate_int_formula
from helper.CustomScript import smtlibscript_from_formula

from pysmt.shortcuts import And, Or, Symbol

class EquivalentTransformer:
    SAT = "sat"
    UNSAT = "unsat"

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
        if (transformationId is None):
            transformationId = random.choices(applicable, weights=[allTransformations.weights[i] for i in applicable], k=1)[0]
        self.substituter.set_transformation(allTransformations.obj_dict[transformationId])
        generating_formula = generate_int_formula(formula) if (generating_formula is None and allTransformations.obj_dict[transformationId].is_generating_transformation()) else generating_formula
        return self.substituter.substitute(formula, generating_formula)

"""
Recursively list subdirectories which contain .smt2-files.
Subdirectories which do not contain .smt2-files are not listed
"""    
def make_subdirectory_list(directoryPath, subdirs):
    added = False
    if (not os.path.exists(directoryPath)):
        raise ValueError("Direcory does not exist.")
    for filename in os.listdir(directoryPath):
        if (not added and filename.endswith(".smt2")):
            added = True
            subdirs.append(directoryPath)
        filePath = os.path.join(directoryPath, filename)
        if (os.path.isdir(filePath)):
            make_subdirectory_list(filePath, subdirs)

"""
Performs a fixed amount of transformations on each formula and tests for satisfiablility after, storing the results in a list.
I would recommend passing a rather high number to the Equivalent Transformer as this determines at which
depth the transformations are done. Since many of the transformations extend the formula (think of e.g. distributivity),
the formula size may explode for a high transformation/substitution-depth.
Passing the option --keep-generated files to the python command stores the generated file in the /generated folder.
""" 
def main():
    parser = SmtLibParser()
    transformer = EquivalentTransformer(20)
    keep_generated_files = len(sys.argv) > 1 and sys.argv[1] == "--keep-generated-files"

    directory = "benchmarks/non-incremental/QF_LIA/20180326-Bromberger/more_slacked/CAV_2009_benchmarks/smt/10-vars"
    relevant_dirs = []
    make_subdirectory_list(directory, relevant_dirs)

    #list of tuples of the form (filename, benchmark_satisfiability, post_transform_satisfiability)
    results = []

    if not os.path.exists("./generated"):
        os.mkdir("./generated")

    for dir in relevant_dirs:
        if not os.path.exists(os.path.join("./generated", dir)):
            os.makedirs(os.path.join("./generated", dir))
        for filename in os.listdir(directory):
            smtFile = open(os.path.join(directory, filename), "r")
            script = parser.get_script(smtFile)
            satisfiability = next(cmd.args[1] for cmd in script.filter_by_command_name([commands.SET_INFO]) if cmd.args[0] == ":status")
            #print(satisfiability)
            formula = script.get_last_formula()

            for i in range(10):
                formula = transformer.transform(formula)
            
            filenameNew = filename.strip(".smt2") + "_gen" + ".smt2"
            script = smtlibscript_from_formula(formula, logic=QF_LIA)
            #daggify inserts a bunch of "let" clauses in the formula, making it way more illegible
            script.to_file(os.path.join("./generated", dir, filenameNew), daggify=False)
            
            result = subprocess.run(['z3', '-file:' + os.path.join("generated", dir, filenameNew)], stdout=subprocess.PIPE)
            results.append((str(os.path.join(dir, filename)), satisfiability, result.stdout.decode('utf-8').strip("\n")))

            if (not keep_generated_files):
                os.remove(os.path.join("generated", dir, filenameNew))
            break
        
    if (not keep_generated_files):
        shutil.rmtree("./generated")


if __name__ == "__main__":
    main()