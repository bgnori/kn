

from reference import Evaluator


import unittest

class TestEvaluator(unittest.TestCase):
    def setUp(self):
        self.ev = Evaluator({})

class TestBasicValues(TestEvaluator):
    def test_empty(self):
        self.assertIsNone(self.ev.eval(""))

    def test_int(self):
        self.assertEqual(self.ev.eval("1"), 1)

    def test_str(self):
        self.assertEqual(self.ev.eval("'str'"), 'str')

    def test_dict(self):
        self.assertEqual(self.ev.eval("{a:1, b: 2}"), {"a": 1, "b": 2})


class TestBuiltin(TestEvaluator):
    def test_add(self):
        self.assertEqual(self.ev.eval("[+, 1, 2]"), 3)

    def test_sub(self):
        self.assertEqual(self.ev.eval("[-, 1, 2]"), -1)

    def test_mul(self):
        self.assertEqual(self.ev.eval("[*, 1, 2]"), 2)


class TestSpecialForms(TestEvaluator):
    def test_let(self):
        self.assertEqual(self.ev.eval("[let, one, 1]"), None)
        self.assertEqual(self.ev.eval("one"), 1)

    def test_quote(self):
        self.assertEqual(self.ev.eval("[quote, [1, 2, 3]]"), [1, 2, 3])

    def test_defn_1(self):
        self.assertEqual(self.ev.eval("[defn, inc, [x], [+, x, 1]]"), None)
        self.assertEqual(self.ev.eval("[inc, 1]"), 2)

    def test_defn_2(self):
        self.assertEqual(self.ev.eval("[defn, sum, [x, y], [+, x, 1]]"), None)
        self.assertEqual(self.ev.eval("[sum, 1, 2]"), 3)


if __name__ == '__main__':
    unittest.main()
