from transformations import AbsorpAnd, AbsorpOr, DeMorgAnd, DeMorgOr, DistrAnd, DistrOr, ExistsNot, ExistsSplit, ForAllNot, ForAllSplit, IdempAnd, IdempOr, LogIdentAnd, LogIdentOr

LOG_IDENT_AND = 0
LOG_IDENT_OR = 1
DISTR_AND = 2
DISTR_OR = 3
DEMORG_AND = 4
DEMORG_OR = 5
ABSORP_AND = 6
ABSORP_OR = 7
IDEMP_AND = 8
IDEMP_OR = 9
EXISTS_NOT = 10
FORALL_NOT = 11
FORALL_SPLIT = 12
EXISTS_SPLIT = 13
##can include rules 7-10 later, these are probably easy to detect

PROP_LOGIC = [i for i in range(10)]
PRED_LOGIC = [i for i in range (10, 13)]
ALL = PROP_LOGIC + PRED_LOGIC

all_dict = {
    LOG_IDENT_AND : LogIdentAnd.LogIdentAnd(),
    LOG_IDENT_OR : LogIdentOr.LogIdentOr(),
    DISTR_AND : DistrAnd.DistrAnd(),
    DISTR_OR : DistrOr.DistrOr(),
    DEMORG_AND : DeMorgAnd.DeMorgAnd(),
    DEMORG_OR : DeMorgOr.DeMorgOr(),
    ABSORP_AND : AbsorpAnd.AbsorpAnd(),
    ABSORP_OR : AbsorpOr.AbsorpOr(),
    IDEMP_AND : IdempAnd.IdempAnd(),
    IDEMP_OR : IdempOr.IdempOr(),
    EXISTS_NOT : ExistsNot.ExistsNot(),
    FORALL_NOT : ForAllNot.ForAllNot(),
    FORALL_SPLIT : ForAllSplit.ForAllSplit(),
    EXISTS_SPLIT : ExistsSplit.ExistsSplit()    
}