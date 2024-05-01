import pysmt.operators as op
from pysmt.formula import FormulaManager

class Substituter:
    manager = FormulaManager()
    placeholder = 1
    
    def __init__(self) -> None:
        #think about how this should be done
        self.fnodeTMap = {
            op.AND: lambda args: self.manager.And(args)
        }
        


class FnodeTMapper:

    def __init__(self, manager: FormulaManager) -> None:
        self.manager = manager

    