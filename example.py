from pysmt.shortcuts import Symbol, LE, GE, Int, And, Equals, Plus, Solver
from pysmt.typing import INT

"""
    For documentation of the pysmt library, see https://pysmt.readthedocs.io/en/latest/api_ref.html

    Methods to be used on formulae can be found at https://pysmt.readthedocs.io/en/latest/api_ref.html#module-pysmt.fnode
"""

hello = [Symbol(s, INT) for s in "hello"]
world = [Symbol(s, INT) for s in "world"]

letters = set(hello+world)

domains = And(And(LE(Int(1), l),
                  GE(Int(10), l)) for l in letters)

sum_hello = Plus(hello)
sum_world = Plus(world)

problem = And(Equals(sum_hello, sum_world),
              Equals(sum_hello, Int(25)))

formula = And(domains, problem)

print("Serialization of the formula:")
print(formula)
for f in domains.args():
    print(f)
print()

for f in domains.get_atoms():
    print(f)

for f in domains.get_free_variables():
    print(f)