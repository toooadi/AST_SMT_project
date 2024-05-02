import unittest
import pysmt.operators as op
import AvailableTransformations as all
from EquivalentTransformer import EquivalentTransformer
from pysmt.shortcuts import And, Or, Not, Exists, ForAll, Symbol

class TestTransformationsSimple(unittest.TestCase):
    transformer = EquivalentTransformer()
    generating_formula = And(Symbol("FV1"), Symbol("FV2"))

    def test_distrAnd(self):
        formula = And(Symbol("A"), Or(Symbol("B"), Symbol("C")))
        self.assertTrue(all.DISTR_AND in self.transformer.get_applicable_transformations(formula))
        self.assertEqual(
            Or(And(Symbol("A"), Symbol("B")), And(Symbol("A"), Symbol("C"))),
            self.transformer.transform(formula, all.DISTR_AND)
        )

    def test_distrOr(self):
        formula = Or(Symbol("A"), And(Symbol("B"), Symbol("C")))
        self.assertTrue(all.DISTR_OR in self.transformer.get_applicable_transformations(formula))
        self.assertEqual(
            And(Or(Symbol("A"), Symbol("B")), Or(Symbol("A"), Symbol("C"))),
            self.transformer.transform(formula, all.DISTR_OR)
        )

    def test_deMorgAnd(self):
        formula = Not(And(Symbol("A"), Symbol("B")))
        self.assertTrue(all.DEMORG_AND in self.transformer.get_applicable_transformations(formula))
        self.assertEqual(
            Or(Not(Symbol("A")), Not(Symbol("B"))),
            self.transformer.transform(formula, all.DEMORG_AND)
        )

    def test_deMorgOr(self):
        formula = Not(Or(Symbol("A"), Symbol("B")))
        self.assertTrue(all.DEMORG_OR in self.transformer.get_applicable_transformations(formula))
        self.assertEqual(
            And(Not(Symbol("A")), Not(Symbol("B"))),
            self.transformer.transform(formula, all.DEMORG_OR)
        )

    def test_logIdentAnd(self):
        formula = Symbol("A")
        self.assertTrue(all.LOG_IDENT_AND in self.transformer.get_applicable_transformations(formula))
        self.assertEqual(
            And(formula, Or(self.generating_formula, Not(self.generating_formula))),
            self.transformer.transform(formula, all.LOG_IDENT_AND, self.generating_formula)
        )

    def test_logIdentOr(self):
        formula = Symbol("A")
        self.assertTrue(all.LOG_IDENT_OR in self.transformer.get_applicable_transformations(formula))
        self.assertEqual(
            Or(formula, And(self.generating_formula, Not(self.generating_formula))),
            self.transformer.transform(formula, all.LOG_IDENT_OR, self.generating_formula)
        )
    
    def test_absorpAnd(self):
        formula = Symbol("A")
        self.assertTrue(all.ABSORP_AND in self.transformer.get_applicable_transformations(formula))
        self.assertEqual(
            And(formula, Or(formula, self.generating_formula)),
            self.transformer.transform(formula, all.ABSORP_AND, self.generating_formula)
        )

    def test_absorpOr(self):
        formula = Symbol("A")
        self.assertTrue(all.ABSORP_OR in self.transformer.get_applicable_transformations(formula))
        self.assertEqual(
            Or(formula, And(formula, self.generating_formula)),
            self.transformer.transform(formula, all.ABSORP_OR, self.generating_formula)
        )

    def test_existsNot(self):
        formula = Exists([Symbol("A")], Not(And(Symbol("A"), Symbol("B"))))
        self.assertTrue(all.EXISTS_NOT in self.transformer.get_applicable_transformations(formula))
        self.assertEqual(
            Not(ForAll([Symbol("A")], And(Symbol("A"), Symbol("B")))),
            self.transformer.transform(formula, all.EXISTS_NOT)
        )

    def test_forAllNot(self):
        formula = ForAll([Symbol("A")], Not(And(Symbol("A"), Symbol("B"))))
        self.assertTrue(all.FORALL_NOT in self.transformer.get_applicable_transformations(formula))
        self.assertEqual(
            Not(Exists([Symbol("A")], And(Symbol("A"), Symbol("B")))),
            self.transformer.transform(formula, all.FORALL_NOT)
        )

    def test_existsSplit(self):
        formula = Exists([Symbol("A")], Or(Symbol("A"), Symbol("B")))
        self.assertTrue(all.EXISTS_SPLIT in self.transformer.get_applicable_transformations(formula))
        self.assertEqual(
            Or(Exists([Symbol("A")], Symbol("A")), Exists([Symbol("A")], Symbol("B"))),
            self.transformer.transform(formula, all.EXISTS_SPLIT)
        )

    def test_forAllSplit(self):
        formula = ForAll([Symbol("A")], And(Symbol("A"), Symbol("B")))
        self.assertTrue(all.FORALL_SPLIT in self.transformer.get_applicable_transformations(formula))
        self.assertEqual(
            And(ForAll([Symbol("A")], Symbol("A")), ForAll([Symbol("A")], Symbol("B"))),
            self.transformer.transform(formula, all.FORALL_SPLIT)
        )
    

if __name__ == '__main__':
    unittest.main()