

from kn.core import Evaluator


import unittest2 as unittest

class TestEvaluator(unittest.TestCase):
    def setUp(self):
        self.ev = Evaluator({})

    def assertIsNone(self, v):
        self.assertEqual(v, None)
    

class TestBasicValues(TestEvaluator):
    def test_empty(self):
        self.assertIsNone(self.ev.run(""))

    def test_int(self):
        self.assertEqual(self.ev.run("1"), 1)

    def test_str(self):
        self.assertEqual(self.ev.run("""'"str"'"""), 'str')

    def test_dict(self):
        self.assertEqual(self.ev.run("{a: 1, b: 2}"), {"a": 1, "b": 2})

    def xtest_list_int(self):
        '''
            must fail. 
        '''
        self.assertEqual(self.ev.run("[1]"), [1])

class TestBuiltin(TestEvaluator):
    def test_add(self):
        self.assertEqual(self.ev.run("[+, 1, 2]"), 3)

    def test_sub(self):
        self.assertEqual(self.ev.run("[-, 1, 2]"), -1)

    def xtest_mul(self):
        '''
            we can't have "[* ..." in yaml
        '''
        self.assertEqual(self.ev.run("[*, 1, 2]"), 2)


class TestSpecialForms(TestEvaluator):
    def test_let(self):
        self.assertEqual(self.ev.run("[let, one, 1, one]"), 1)

    def test_quote(self):
        self.assertEqual(self.ev.run("[quote, [1, 2, 3]]"), [1, 2, 3])

    def test_define(self):
        self.assertEqual(self.ev.run("[define, one_plus_one, [+, 1, 1]]"), None)
        self.assertEqual(self.ev.run("one_plus_one"), 2)

    def test_defn_1(self):
        self.assertEqual(self.ev.run("[defn, inc, [x], [+, x, 1]]"), None)
        self.assertEqual(self.ev.run("[inc, 1]"), 2)

    def test_defn_2(self):
        self.assertEqual(self.ev.run("[defn, sum, [x, y], [+, x, y]]"), None)
        self.assertEqual(self.ev.run("[sum, 1, 2]"), 3)

    def test_inplace_call_with_fn(self):
        self.assertEqual(self.ev.run("[[fn, [x], [+, x, 1]], 2]"), 3)

class TestClosure(TestEvaluator):

    def test_inplace_call_with_fn(self):
        self.assertEqual(self.ev.run("[[fn, [x], [+, x, 1]], 2]"), 3)
    

if __name__ == '__main__':
    unittest.main()
