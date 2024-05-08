import pysmt.operators as op
from pysmt.formula import FormulaManager
from transformations.Transformation import Transformation
from pysmt.shortcuts import get_env

class FirstOccurenceSubstituter:
    manager = FormulaManager(get_env())

    def __init__(self, transformation: Transformation) -> None:
        self.transformation = transformation
        self.mapper = FnodeTMapper(self.manager)
        self.substituted = False

    def set_transformation(self, transformation:Transformation):
        self.transformation = transformation
        self.manager = FormulaManager(get_env())
        self.substituted = False
    
    def substitute(self, formula, generating_formula=None):
        if (self.substituted):
            return formula

        if (self.transformation.is_directly_applicable(formula)):
            self.substituted = True
            return self.transformation.apply(formula) if (not generating_formula) else self.transformation.apply(formula, generating_formula)
        
        sub_function = self.mapper.get_sub_function(formula.node_type())
        if (sub_function):
            return sub_function(formula, [self.substitute(f, generating_formula) for f in formula.args()])
        
        #Last case: any literal will obviously not be substituted
        return formula

#substitutes at the first transformable occurence at depth >= subDepth
#If there is no substitution at the aspired depth, the deepest transformable formula will be substituted
class NDepthSubstituter(FirstOccurenceSubstituter):

    def __init__(self, transformation: Transformation, subDepth) -> None:
        super().__init__(transformation)
        self.subDepth = subDepth
        self.currentDepth = -1

    def set_transformation(self, transformation: Transformation):
        super().set_transformation(transformation)
        self.currentDepth = -1

    def set_subDepth(self, subDepth):
        self.subDepth = subDepth

    def substitute(self, formula, generating_formula=None):
        try:
            if (self.substituted):
                return formula
            
            self.currentDepth += 1

            if (self.transformation.is_directly_applicable(formula)):
                if (self.currentDepth >= self.subDepth):
                    self.substituted = True
                    return self.transformation.apply(formula) if (not generating_formula) else self.transformation.apply(formula, generating_formula)
                
                sub_function = self.mapper.get_sub_function(formula.node_type())
                if (sub_function):
                    children = [self.substitute(f, generating_formula) for f in formula.args()]
                    if (self.substituted):
                        return sub_function(formula, children)
                    else:
                        self.substituted = True
                        return self.transformation.apply(formula) if (not generating_formula) else self.transformation.apply(formula, generating_formula)
            
            sub_function = self.mapper.get_sub_function(formula.node_type())
            if (sub_function):
                return sub_function(formula, [self.substitute(f, generating_formula) for f in formula.args()])

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
            op.EXISTS : self.subExists
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
