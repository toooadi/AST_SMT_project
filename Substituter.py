import pysmt.operators as op
from pysmt.formula import FormulaManager
from transformations.Transformation import Transformation
from pysmt.shortcuts import get_env
from helper.FormulaHelper import find_maxDepth
import random
import AvailableWeakeningsStrengthenings as allWeakeningsStrengthenings

SAT = "sat"
UNSAT = "unsat"

class FirstOccurenceSubstituter:
    manager = FormulaManager(get_env())

    def __init__(self, transformation: Transformation) -> None:
        self.transformation = transformation
        self.mapper = FnodeTMapper(self.manager)
        self.substituted = False

    def set_transformation(self, transformation:Transformation):
        self.transformation = transformation
        self.manager = FormulaManager(get_env())
        self.mapper = FnodeTMapper(self.manager)
        self.substituted = False
    
    def substitute(self, formula, generating_formula=None):
        if (self.substituted):
            return formula

        if (self.transformation.is_directly_applicable(formula)):
            self.substituted = True
            return self.transformation.apply(formula) if (not generating_formula) else self.transformation.apply(formula, generating_formula)
        
        #maybe put this before the directly_applicable check if it is slow
        sub_function = self.mapper.get_sub_function(formula.node_type())
        if (sub_function):
            return sub_function(formula, [self.substitute(f, generating_formula) for f in formula.args()])
        
        #Last case: any literal will obviously not be substituted
        return formula
        
"""
substitutes at the first transformable occurence at depth >= subDepth
If there is no substitution at the aspired depth, the deepest transformable formula will be substituted
"""
class NDepthSubstituter(FirstOccurenceSubstituter):

    def __init__(self, transformation: Transformation, subDepth, doShuffling=False) -> None:
        super().__init__(transformation)
        self.subDepth = subDepth
        self.currentDepth = -1
        self.maxDepth = -1
        self.doShuffling = doShuffling

    def set_transformation(self, transformation: Transformation):
        super().set_transformation(transformation)
        self.currentDepth = -1
        self.maxDepth = -1

    def set_subDepth(self, subDepth):
        self.subDepth = subDepth

    #max_depth is first calculated, then transform only on max depth if smaller than subDepth
    def substitute(self, formula, generating_formula=None):
        self.maxDepth = find_maxDepth(formula, -1)
        return self.substitute_walker(formula, generating_formula)

    #Do the actual substitution work
    def substitute_walker(self, formula, generating_formula):
        try:
            if (self.substituted):
                return formula
            
            self.currentDepth += 1

            if (self.currentDepth >= self.subDepth and self.transformation.is_directly_applicable(formula)):
                self.substituted = True
                return self.transformation.apply(formula) if (not generating_formula) else self.transformation.apply(formula, generating_formula)
            elif (self.currentDepth >= self.maxDepth and self.transformation.is_directly_applicable(formula)):
                self.substituted = True
                return self.transformation.apply(formula) if (not generating_formula) else self.transformation.apply(formula, generating_formula)
            else:
                sub_function = self.mapper.get_sub_function(formula.node_type())
                if (sub_function):
                    children = formula.args()
                    if (self.doShuffling and self.currentDepth == 0 and random.randrange(4) == 0):
                        children = list(children)
                        #avoid always transforming the first line, shouldn't be too expensive since there's mostly a small number of children
                        random.shuffle(children)
                    return sub_function(formula, [self.substitute_walker(f, generating_formula) for f in children])
                
            return formula

        finally:
            self.currentDepth -= 1

def is_weakenable_strengthenable(formula):
    return (formula.is_not() and formula.arg(0).is_equals()) or formula.is_lt() or formula.is_le() or formula.is_equals()


class DeepWeakenerStrengthener:
    manager = FormulaManager(get_env())

    def __init__(self, doShuffling=False) -> None:
        self.doShuffling = doShuffling
        self.satisfiability = ""
        self.substituted = False
        self.mapper = FNodeTMapperExt(self.manager)
        self.currentDepth = -1

    def set_satisfiability(self, satisfiability):
        self.currentDepth = -1
        self.substituted = False
        self.satisfiability = satisfiability
        self.manager = FormulaManager(get_env())
        self.mapper = FNodeTMapperExt(self.manager)
    
    def substitute(self, formula, parity):
        try:
            self.currentDepth += 1

            if (self.substituted):
                return formula
            
            if (is_weakenable_strengthenable(formula)):
                candidates = allWeakeningsStrengthenings.STRENGTHEN if (self.satisfiability == SAT and parity < 0) or (self.satisfiability == UNSAT and parity > 0) else allWeakeningsStrengthenings.WEAKEN
                candidates = [c for c in candidates if c.is_directly_applicable(formula)]
                transformation = random.choice(candidates)
                self.substituted = True
                return transformation.apply(formula)

            if(formula.is_not()):
                return self.manager.Not(self.substitute(formula.arg(0), parity * -1))
            
            if (formula.is_implies()):
                return self.substitute(self.manager.Or(self.manager.Not(formula.arg(0)), formula.arg(1)), parity)
            
            if (formula.is_iff()):
                return self.substitute(self.manager.Or(self.manager.And(formula.arg(0), formula.arg(1)), self.manager.And(self.manager.Not(formula.arg(0)), self.manager.Not(formula.arg(1)))), parity)
            
            sub_function = self.mapper.get_sub_function(formula.node_type())
            if (sub_function and (formula.is_and() or formula.is_or() or formula.is_exists())):
                children = list(formula.args())
                if (self.doShuffling and self.currentDepth == 0):
                    random.shuffle(children)

                return sub_function(formula, [self.substitute(f, parity) for f in children])

            return formula
        
        finally:
            self.currentDepth -= 1


    

class FnodeTMapper:

    def __init__(self, manager: FormulaManager) -> None:
        self.manager = manager
        self.map = {
            op.AND : self.subAnd,
            op.OR : self.subOr,
            op.NOT : self.subNot,
            op.FORALL : self.subForAll,
            op.EXISTS : self.subExists,
            op.IMPLIES : self.subImplies,
            op.IFF : self.subIff
        }

    def get_sub_function(self, op):
        try:
            return self.map[op]
        except KeyError:
            return None

    def subAnd(self, formula, args):
        return self.manager.And(args)
    
    def subOr(self, formula, args):
        return self.manager.Or(args)
    
    def subNot(self, formula, args):
        return self.manager.Not(args[0])
    
    def subForAll(self, formula, args):
        return self.manager.ForAll([f for f in formula.quantifier_vars()], args[0])
    
    def subExists(self, formula, args):
        return self.manager.Exists([f for f in formula.quantifier_vars()], args[0])
    
    def subImplies(self, formula, args):
        return self.manager.Implies(args[0], args[1])
    
    def subIff(self, formula, args):
        return self.manager.Iff(args[0], args[1])


class FNodeTMapperExt(FnodeTMapper):
    
    def __init__(self, manager: FormulaManager) -> None:
        super().__init__(manager)
        extMap = {
            op.LE: self.subLE,
            op.LT: self.subLT,
            op.EQUALS: self.subEq
        }
        self.map.update(extMap)

    def subLE(self, formula, args):
        return self.manager.LE(args[0], args[1])
    
    def subLT(self, formula, args):
        return self.manager.LT(args[0], args[1])
    
    def subEq(self, formula, args):
        return self.manager.Equals(args[0], args[1])