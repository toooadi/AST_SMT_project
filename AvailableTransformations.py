LOG_IDENT = 0
DISTRIB = 1
DEMORG = 2
ABSORP = 3
IDEMP = 4
NOT_FORALL = 5
EXISTS_NOT = 6
NOT_EXISTS = 7
FORALL_NOT = 8
FORALL_SPLIT = 9
EXISTS_SPLIT = 10
FORALL_SWAP = 11
EXISTS_SWAP = 12
##can include rules 7-10 later, these are probably easy to detect

PROP_LOGIC = [i for i in range(5)]
PRED_LOGIC = [i for i in range (5, 11)]
ALL = PROP_LOGIC + PRED_LOGIC