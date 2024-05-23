import multiprocessing.queues
import AvailableEquivalenceTransformations as allTransformations
import random
import os
import multiprocessing
import z3
import time
import queue
from datetime import datetime
from Substituter import FirstOccurenceSubstituter, NDepthSubstituter
from pysmt.smtlib.parser import SmtLibParser
import pysmt.smtlib.commands as commands
import shutil
import sys
from helper.FormulaHelper import generate_formula, solve_smt2_file
from helper.CustomScript import smtlibscript_from_formula
from helper.DirectoryHelper import make_subdirectory_list

NUM_TRANSFORMATIONS = 10
NUM_PROCESSES = 8
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
        generating_formula = generate_formula(formula) if (generating_formula is None and allTransformations.obj_dict[transformationId].is_generating_transformation()) else generating_formula
        return self.substituter.substitute(formula, generating_formula)

def prepend_satisfiability(filename, satisfiability):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write("(set-info :status " + satisfiability + ")\n" + content)

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
    

def transform_and_solve(file_queue, result_queue, subDepth, doShuffling, keep_generated_files, measure_original_solving_time):
    parser = SmtLibParser()
    transformer = EquivalentTransformer(subDepth=subDepth, doShuffling=doShuffling)
    file_path = ""
    
    while not file_queue.empty():
        try:
            file_path = file_queue.get_nowait()
            smt_file = open(file_path, "r")
            script = parser.get_script(smt_file)

            satisfiability = next(cmd.args[1] for cmd in script.filter_by_command_name([commands.SET_INFO]) if cmd.args[0] == ":status")
            original_solving_time = -1
            if (measure_original_solving_time):
                satisfiability, original_solving_time = solve_smt2_file(file_path, Z3_TIMEOUT)

            formula = script.get_last_formula()

            for _ in range(NUM_TRANSFORMATIONS):
                formula = transformer.transform(formula)

            script = smtlibscript_from_formula(formula)
            #daggify inserts a bunch of "let" clauses in the formula, making it way more illegible
            script.to_file(os.path.join("generated", file_path), daggify=False)

            result_sat, solving_time_transformed = solve_smt2_file(os.path.join("generated", file_path), Z3_TIMEOUT)
            result_queue.put((file_path, satisfiability, result_sat, original_solving_time, solving_time_transformed))
            prepend_satisfiability(os.path.join("generated", file_path), result_sat)

            if (not keep_generated_files):
                os.remove(os.path.join("generated", file_path))
            
            smt_file.close()
            print("Processed " + file_path.split("/")[-1])

        except queue.Empty:
            time.sleep(random.random())
        except NotImplementedError as e:
            smt_file.close()
            if (str(e).startswith("Unknown function")):
                continue
            else:
                print(str(e) + "in file " + file_path.split("/")[-1])
        except Exception as e:
            smt_file.close()
            print(str(e) + "in file " + file_path.split("/")[-1])
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

    os.makedirs("generated", exist_ok=True)

    for dir in relevant_dirs:
        os.makedirs(os.path.join("generated", dir), exist_ok=True)
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

    print("All files processed. Printing to file.")
    while not result_queue.empty():
        results.append(result_queue.get())

    os.makedirs("results", exist_ok=True)
    with open(os.path.join("results", "run_" + datetime.now().strftime("%d-%m-%Y__%H%M") + ".txt"), "w") as f:
        print("transformations:" + str(NUM_TRANSFORMATIONS) + ", subDepth: " + str(subDepth) + ", doShuffling: " + str(doShuffling) + ", dir: " + directory, file=f)
        for result in results:
            print(result, file=f)

    
        
    if (not keep_generated_files):
        shutil.rmtree("./generated")

    



if __name__ == "__main__":
    main()