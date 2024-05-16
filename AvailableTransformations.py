from transformations import AbsorpAnd, AbsorpOr, DeMorgAnd, DeMorgOr, DistrAnd, DistrOr, ExistsNot, ExistsSplit, ForAllNot, ForAllSplit, IdempAnd, IdempOr, LogIdentAnd, LogIdentOr, DoubleNeg

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
DOUBLE_NEG = 10
EXISTS_NOT = 11
FORALL_NOT = 12
FORALL_SPLIT = 13
EXISTS_SPLIT = 14
##can include rules 7-10 later, these are probably easy to detect

PROP_LOGIC = [i for i in range(11)]
PRED_LOGIC = [i for i in range (10, 15)]
ALL = PROP_LOGIC + PRED_LOGIC

obj_dict = {
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
    DOUBLE_NEG : DoubleNeg.DoubleNeg(),
    EXISTS_NOT : ExistsNot.ExistsNot(),
    FORALL_NOT : ForAllNot.ForAllNot(),
    FORALL_SPLIT : ForAllSplit.ForAllSplit(),
    EXISTS_SPLIT : ExistsSplit.ExistsSplit()    
}

#This determines the weights of the operations. Operations which are always applicable will have a lower weight
#so that when a more rarely applicable operation IS available, it is picked with a higher probability.
weights = {
    LOG_IDENT_AND : 1,
    LOG_IDENT_OR : 2,
    DISTR_AND : 7,
    DISTR_OR : 7,
    DEMORG_AND : 10,
    DEMORG_OR : 10,
    ABSORP_AND : 1,
    ABSORP_OR : 2,
    IDEMP_AND : 1,
    IDEMP_OR : 2,
    DOUBLE_NEG : 4,
    EXISTS_NOT : 10,
    FORALL_NOT : 10,
    FORALL_SPLIT : 10,
    EXISTS_SPLIT : 10    
}