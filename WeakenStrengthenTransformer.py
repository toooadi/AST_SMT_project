import multiprocessing
import multiprocessing.queues
import os
import queue
import random
import sys
import time
from datetime import datetime

import pysmt.smtlib.commands as commands
from pysmt.smtlib.parser import SmtLibParser

from helper.CustomScript import smtlibscript_from_formula
from helper.DirectoryHelper import make_subdirectory_list
from helper.FormulaHelper import solve_smt2_file
from Substituter import DeepWeakenerStrengthener

SAT = "sat"
UNSAT = "unsat"
NUM_TRANSFORMATIONS = 10
Z3_TIMEOUT = 90000
NUM_PROCESSES = 8

def transform_and_solve(file_queue, result_queue, doShuffling, keep_generated_files, solver="z3"):
    parser = SmtLibParser()
    substituter = DeepWeakenerStrengthener(doShuffling=doShuffling)
    file_path = ""

    try:
        while not file_queue.empty():
            try:
                file_path = file_queue.get_nowait()
                smt_file = open(file_path, "r")
                script = parser.get_script(smt_file)

                satisfiability = next(cmd.args[1] for cmd in script.filter_by_command_name([commands.SET_INFO]) if cmd.args[0] == ":status")
                
                formula = script.get_last_formula()

                substituter.set_satisfiability(satisfiability)
                for _ in range(NUM_TRANSFORMATIONS):
                    formula = substituter.substitute(formula, 1)

                script = smtlibscript_from_formula(formula)
                #daggify inserts a bunch of "let" clauses in the formula, making it way more illegible
                script.to_file(os.path.join("generated", "weakenedStrengthened", file_path), daggify=False)

                result_sat, solving_time_transformed = solve_smt2_file(os.path.join("generated", "weakenedStrengthened", file_path), Z3_TIMEOUT, solver=solver)
                result_queue.put((file_path.split("/")[-1], satisfiability, result_sat, solving_time_transformed))

                if (not keep_generated_files):
                    os.remove(os.path.join("generated", "weakenedStrengthened", file_path))
                
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
    finally:
        #need this, deadlock for long executions otherwise
        result_queue.cancel_join_thread()

def parse_args():
    try:
        keep_generated_files = "--keep-generated-files" in sys.argv
        doShuffling = "--do-shuffling" in sys.argv
        directory = next(i for i in sys.argv if i.startswith("--dir")).split("=")[1]
        solver = next(i for i in sys.argv if i.startswith("--solver")).split("=")[1]
        return keep_generated_files, doShuffling, directory, solver
    except:
        raise ValueError("Badly formatted arguments. Check for spelling mistakes and validity of passed directories.")

def main():
    keep_generated_files, doShuffling, directory, solver = parse_args()
    relevant_dirs = []
    make_subdirectory_list(directory, relevant_dirs)
    filepath_queue = multiprocessing.Queue()

    #list of tuples of the form (filename, preWeakeningStrengthening_satisfiability, post_transform_satisfiability, post_transform_solving_time)
    results = []
    result_queue = multiprocessing.Queue()

    os.makedirs("generated", exist_ok=True)

    for dir in relevant_dirs:
        os.makedirs(os.path.join("generated", "weakenedStrengthened", dir), exist_ok=True)
        for filename in os.listdir(dir):
            if filename.endswith(".smt2"):
                filepath_queue.put(os.path.join(dir, filename))


    processes = []
    for _ in range(NUM_PROCESSES):
        process = multiprocessing.Process(target=transform_and_solve, args=(filepath_queue, result_queue, doShuffling, keep_generated_files, solver))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print("All files processed. Printing to file.")
    while not result_queue.empty():
        results.append(result_queue.get())

    os.makedirs("results/weakenedStrengthened", exist_ok=True)
    with open(os.path.join("results", "weakenedStrengthened", "run_" + datetime.now().strftime("%d-%m-%Y__%H%M") + ".txt"), "w") as f:
        print("transformations:" + str(NUM_TRANSFORMATIONS) + ", doShuffling: " + str(doShuffling) + ", dir: " + directory + ", solver:" + solver, file=f )
        for result in results:
            print(result, file=f)

if __name__ == "__main__":
    main()