LOG_IDENT = 0
DISTRIB = 1
DEMORGANS = 2
ABSORP = 3
IDEMP = 4
NOT_FORALL = 5
NOT_EXISTS = 6
FORALL_SPLIT = 7
EXISTS_SPLIT = 8
FORALL_SWAP = 9
EXISTS_SWAP = 10
##can include rules 7-10 later, these are probably easy to detect

PROP_LOGIC = [i for i in range(5)]
PRED_LOGIC = [i for i in range (5, 11)]
ALL = PROP_LOGIC + PRED_LOGIC