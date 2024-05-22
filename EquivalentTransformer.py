import multiprocessing.queues
import AvailableTransformations as allTransformations
import random
import os
import multiprocessing
import z3
import time
import queue
from Substituter import FirstOccurenceSubstituter, NDepthSubstituter
from pysmt.smtlib.parser import SmtLibParser
import pysmt.smtlib.commands as commands
from pysmt.logics import QF_LIA, QF_LRA, QF_NIA, LIA
import subprocess
import shutil
import sys
from helper.FormulaHelper import generate_int_formula
from helper.CustomScript import smtlibscript_from_formula

NUM_TRANSFORMATIONS = 10
NUM_PROCESSES = 4
Z3_TIMEOUT = 90000

class EquivalentTransformer:
    SAT = "sat"
    UNSAT = "unsat"

    """
    main class to fetch the formulas and perform equivalence transformations on them
    """

    def __init__(self, subDepth=None, doShuffling=False) -> None:
        if (subDepth):
            self.substituter = NDepthSubstituter(None, subDepth, doShuffling=doShuffling) # type: ignore
        else:
            self.substituter = FirstOccurenceSubstituter(None) # type: ignore

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

def parse_args():
    try:
        keep_generated_files = "--keep-generated-files" in sys.argv
        doShuffling = "--do-shuffling" in sys.argv
        measure_original_solving_time = "--measure_original_solving_time" in sys.argv
        directory = next(i for i in sys.argv if i.startswith("--dir")).split("=")[1]
        subDepthFullArg = next((i for i in sys.argv if i.startswith("--sub-depth")), None)
        subDepth = int(subDepthFullArg.split("=")[1]) if subDepthFullArg else 0
        return keep_generated_files, doShuffling, directory, subDepth, measure_original_solving_time

    except:
        raise ValueError("Badly formatted arguments. Check for spelling mistakes and validity of passed directories.")
    
def solve_smt2_file(filePath):
    try:
        solver = z3.Solver()
        solver.add(z3.parse_smt2_file(filePath))
        solver.set("timeout", Z3_TIMEOUT)

        start_time = time.time()
        result = solver.check()
        end_time = time.time()

        result_string = "sat" if result == z3.sat else "unsat" if result == z3.unsat else "timeout" if solver.reason_unknown() == "timeout" else "unknown"
        return result_string, end_time - start_time
    
    except  Exception:
        return "Error", 0

def transform_and_solve(file_queue, result_queue, subDepth, doShuffling, keep_generated_files, measure_original_solving_time):
    parser = SmtLibParser()
    transformer = EquivalentTransformer(subDepth=subDepth, doShuffling=doShuffling)
    
    while not file_queue.empty():
        try:
            file_path = file_queue.get_nowait()
            smt_file = open(file_path, "r")
            script = parser.get_script(smt_file)

            satisfiability = next(cmd.args[1] for cmd in script.filter_by_command_name([commands.SET_INFO]) if cmd.args[0] == ":status")
            original_solving_time = -1
            if (measure_original_solving_time):
                satisfiability, original_solving_time = solve_smt2_file(file_path)

            formula = script.get_last_formula()

            for _ in range(NUM_TRANSFORMATIONS):
                formula = transformer.transform(formula)

            script = smtlibscript_from_formula(formula)
            #daggify inserts a bunch of "let" clauses in the formula, making it way more illegible
            script.to_file(os.path.join("generated", file_path), daggify=False)

            result_sat, solving_time_transformed = solve_smt2_file(os.path.join("generated", file_path))
            result_queue.put((file_path, satisfiability, result_sat, original_solving_time, solving_time_transformed))

            if (not keep_generated_files):
                os.remove(os.path.join("generated", file_path))
            
            print("Processed " + file_path.split("/")[-1])

        except queue.Empty:
            continue
    #need this, deadlock for long executions otherwise
    result_queue.cancel_join_thread()

        



"""
Performs a fixed amount of transformations on each formula and tests for satisfiablility after, storing the results in a list.
I would recommend passing a rather high number to the Equivalent Transformer as this determines at which
depth the transformations are done. Since many of the transformations extend the formula (think of e.g. distributivity),
the formula size may explode for a high transformation/substitution-depth.
AVAILABLE OPTIONS:
--dir=<benchmark directory> : MANDATORY, specifies the benchmark directory to be tested. Can be relative to project folder.
--sub-depth=<substitution Depth as int> : VERY RECOMMENDED (high number), determines the depth at which the substitution should be performed, if possible
--keep-generated-files : keeps the newly generated files in a dedicated /generated/ directory
--do-shuffling : RECOMMENDED, occasionally shuffles the top level formula so that it's not always the same subformula being modified
""" 
def main():
    keep_generated_files, doShuffling, directory, subDepth, measure_original_solving_time = parse_args()

    #directory = "benchmarks/non-incremental/QF_LIA/20180326-Bromberger/more_slacked/CAV_2009_benchmarks/smt/10-vars"
    relevant_dirs = []
    make_subdirectory_list(directory, relevant_dirs)
    filepath_queue = multiprocessing.Queue()

    #list of tuples of the form (filename, benchmark_satisfiability, post_transform_satisfiability, pre_transform_solving_time, post_transform_solving_time)
    #pre_transform_solving_time is -1 if it is not measured
    results = []
    result_queue = multiprocessing.Queue()

    if not os.path.exists("./generated"):
        os.mkdir("./generated")

    for dir in relevant_dirs:
        if not os.path.exists(os.path.join("./generated", dir)):
            os.makedirs(os.path.join("./generated", dir))
        for filename in os.listdir(dir):
            if filename.endswith(".smt2"):
                filepath_queue.put(os.path.join(dir, filename))

    print(filepath_queue.qsize())

    processes = []
    for _ in range(NUM_PROCESSES):
        process = multiprocessing.Process(target=transform_and_solve, args=(filepath_queue, result_queue, subDepth, doShuffling, keep_generated_files, measure_original_solving_time))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print("joined all")
    while not result_queue.empty():
        results.append(result_queue.get())
        
    if (not keep_generated_files):
        shutil.rmtree("./generated")

    



if __name__ == "__main__":
    main()