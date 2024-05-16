from pysmt.smtlib.script import SmtLibCommand, SmtLibScript
import warnings
import pysmt.smtlib.commands as smtcmd
from pysmt.exceptions import (NoLogicAvailableError,
                              UndefinedLogicError)
from pysmt.oracles import get_logic
from pysmt.logics import get_closer_smtlib_logic, Logic, SMTLIB2_LOGICS
from pysmt.environment import get_env

#small adaptation where asserts will be split up to increase readability
def smtlibscript_from_formula(formula, logic=None):
    script = SmtLibScript()

    if logic is None:
        # Get the simplest SmtLib logic that contains the formula
        f_logic = get_logic(formula)

        smt_logic = None
        try:
            smt_logic = get_closer_smtlib_logic(f_logic)
        except NoLogicAvailableError:
            warnings.warn("The logic %s is not reducible to any SMTLib2 " \
                          "standard logic. Proceeding with non-standard " \
                          "logic '%s'" % (f_logic, f_logic),
                          stacklevel=3)
            smt_logic = f_logic
    elif not (isinstance(logic, Logic) or isinstance(logic, str)):
        raise UndefinedLogicError(str(logic))
    else:
        if logic not in SMTLIB2_LOGICS:
            warnings.warn("The logic %s is not reducible to any SMTLib2 " \
                          "standard logic. Proceeding with non-standard " \
                          "logic '%s'" % (logic, logic),
                          stacklevel=3)
        smt_logic = logic

    script.add(name=smtcmd.SET_LOGIC,
               args=[smt_logic])

    # Declare all types
    types = get_env().typeso.get_types(formula, custom_only=True)
    for type_ in types:
        script.add(name=smtcmd.DECLARE_SORT, args=[type_.decl])

    deps = formula.get_free_variables()
    # Declare all variables
    for symbol in deps:
        assert symbol.is_symbol()
        script.add(name=smtcmd.DECLARE_FUN, args=[symbol])

    # Assert formula
    if (formula.is_and()):
        for f in formula.args():
            script.add_command(SmtLibCommand(name=smtcmd.ASSERT,
                                             args=[f]))
    else:
        script.add_command(SmtLibCommand(name=smtcmd.ASSERT,
                                        args=[formula]))

    # check-sat
    script.add_command(SmtLibCommand(name=smtcmd.CHECK_SAT,
                                     args=[]))
    return script