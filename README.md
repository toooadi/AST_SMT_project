# Project setup:

Install the necessary prerequisites to run the testing tool:

`pip install pysmt`

`pip install z3-solver`

Fetch the testing benchmarks. The SMT-LIB benchmarks are located in the **/benchmarks/** directory while the YinYang testing suite can be found under **/semantic-fusion-seeds/**
> bash ./fetch_benchmarks.sh


# Running the testing tool

*Note: The tool was built on Pyton 3.11.9. You might experience issues when using newer versions due to incompatibilities in pysmt*

The tool is ran using the normal python run command and is divided in two parts.
*Hint: To make use of cvc5, you must download the executable and put it into your PATH: https://github.com/cvc5/cvc5/releases/*

<br/><br/>

`EquivalentTransformer.py` performs the equivalence transformations and stores the transformed formulae under **/generated/** (if needed). You can pass it the following options (make sure they're spelled correctly):

`--dir=<benchmark directory>` : MANDATORY, specifies the benchmark directory to be tested. Can be relative to project folder.

`--sub-depth=<substitution Depth as int>` : VERY RECOMMENDED (high number), determines the depth at which the substitution should be performed, if possible

`--keep-generated-files` : keeps the newly generated files in a dedicated /generated/ directory

`--do-shuffling` : RECOMMENDED, occasionally shuffles the top level formula so that it's not always the same subformula being modified

`--measure-original-solving-time` : measures the solving time of the original formula before the transformations are applied. Implies one more call to a solver. Otherwise the original solving times in the results will be -1

`--solver=<solver>` : specifies the solver to be used for solving the formulas, default is z3. Options are z3 and cvc5. The latter must be installed first (see hint above)
  
<br/><br/>

`WeakenStrengthenTransformer.py` is our adaptation of Weakening and Strengthening which is originally described in the paper by Bringolf et al. where they came up with their testing tool Janus. It take the following similar arguments:

`--dir`=<benchmark directory> : MANDATORY, specifies the benchmark directory to be tested. Can be relative to project folder.

`--keep-generated-files` : keeps the newly generated files in a dedicated /generated/ directory

`--do-shuffling` : RECOMMENDED, occasionally shuffles the top level formula so that it's not always the same subformula being modified.

`--solver=<solver>` : specifies the solver to be used for solving the formulas. Options are z3 and cvc5. The latter must be installed first (see hint above)

Example command:

> python EquivalentTransformer.py --sub-depth=10 --do-shuffling --dir=semantic-fusion-seeds/LIA/sat --keep-generated-files

Both transformers store a file containing their respective results in **/results/**.