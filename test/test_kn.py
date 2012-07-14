from kn.core import Evaluator
from kn.core import NotInvokableError, UnboundError, RuntimeError

import unittest2 as unittest

class TestSmoke(unittest.TestCase):
    def assertin(self, d, k):
        self.assert_(k in d)

    def test_new_without_param(self):
        e = Evaluator()
        self.assertin(e.scope.top(), 'evaluator')

    def test_new_with_param(self):
        e = Evaluator({1: 1})
        self.assertin(e.scope.top(), 'evaluator')
        self.assertin(e.scope.top(), 1)


class TestEvaluator(unittest.TestCase):
    def setUp(self):
        self.ev = Evaluator({})
    

class TestBasicValues(TestEvaluator):
    def test_empty(self):
        self.assertIsNone(self.ev.run(""))

    def test_int(self):
        self.assertEqual(self.ev.run("1"), 1)

    def test_identifier(self):
        self.assertRaises(UnboundError, self.ev.run, "str")

    def test_str(self):
        self.assertEqual(self.ev.run("""'"str"'"""), 'str')

    def test_str(self):
        self.assertEqual(self.ev.run("""'"str"'"""), 'str')

    def test_dict(self):
        self.assertEqual(self.ev.run("{a: 1, b: 2}"), {"a": 1, "b": 2})

    def test_list_int(self):
        self.assertRaises(NotInvokableError, self.ev.run, "[1]")


class TestBuiltin(TestEvaluator):
    def test_prn(self):
        self.assertEqual(self.ev.run("[prn, 1,]"), None)

    def test_add(self):
        self.assertEqual(self.ev.run("[+, 1, 2]"), 3)

    def test_sub(self):
        self.assertEqual(self.ev.run("[-, 1, 2]"), -1)

    def test_eq_t(self):
        self.assertEqual(self.ev.run("[eq, 1, 1]"), True)

    def test_eq_f(self):
        self.assertEqual(self.ev.run("[eq, 1, 2]"), False)
    
    def test_le(self):
        self.assertEqual(self.ev.run("[le, 1, 2]"), True)

    def test_gt(self):
        self.assertEqual(self.ev.run("[gt, 1, 2]"), False)

    def test_mul(self):
        '''
            we can't have "[* ..." in yaml
        '''
        self.assertEqual(self.ev.run("[mul, 1, 2]"), 2)

    def test_file(self):
        self.ev.run("""[define, f, [open, '"hello.yaml"']]""")
        self.assertEqual(self.ev.run("[read, f]"), "[hello, kn!]\n")
        self.ev.run("[close, f]")

    def test_eval(self):
        self.ev.run("""[define, f, [open, '"test/boo.yaml"']]""")
        self.ev.run("[define, toload, [read, f]]")
        self.ev.run("[close, f]")
        self.assertEqual(self.ev.run("[eval, [parse, toload]]"), 3)


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

    def test_if_t(self):
        self.assertEqual(self.ev.run("""[if, 1, '"True"', '"False"']"""), 'True')

    def test_if_f(self):
        self.assertEqual(self.ev.run("""[if, 0, '"True"', '"False"']"""), 'False')

    def test_if_nested_a(self):
        self.assertEqual(self.ev.run("""[if, 1, '"A"', [if,  1, [would not be evaluated],  [would not be evaluated]]]"""), 'A')

    def test_if_nested_b(self):
        self.assertEqual(self.ev.run("""[if, 0, '"A"', [if,  1, '"B"',  [would not be evaluated]]]"""), 'B')

    def test_if_nested_c(self):
        self.assertEqual(self.ev.run("""[if, 0, '"A"', [if,  0, [would not be evaluated], '"C"']]"""), 'C')


class TestClosure(TestEvaluator):
    def test_invoke(self):
        self.assertRaises(NotInvokableError, self.ev.run, "[{}]")

    def test_inplace_call_with_fn(self):
        self.assertEqual(self.ev.run("[[fn, [x], [+, x, 1]], 2]"), 3)

    def test_recursion_fact(self):
        self.ev.run("[defn, fact, [x], [if, [eq, x, 0], 1, [mul, x, [fact, [-, x, 1]]]]]")
        self.assertEqual(self.ev.run("[fact, 5]"), 120)

    def test_recursion_tarai(self):
        self.ev.run("""[defn, tarai, [x, y, z], 
                          [if, [gt, x, y], 
                            [tarai, [tarai, [-, x, 1], y, z], [tarai, [-, y, 1], z, x], [tarai, [-, z, 1], x, y]],
                            y]]""")
        self.assertEqual(self.ev.run("[tarai, 4, 3, 0]"), 4)


class TestDefineFnWithFib(TestEvaluator):
    def setUp(self):
        super(TestDefineFnWithFib, self).setUp()
        self.ev.run("""[define, fib, [fn, [x], 
                      [if, [eq, x, 1], 
                            1, 
                      [if, [eq, x, 2], 
                            1, 
                           [+, [fib, [-, x, 1]], [fib, [-, x, 2]]]]]]]""")

    def test_1(self):
        self.assertEqual(self.ev.run("[fib, 1]"), 1)

    def test_2(self):
        self.assertEqual(self.ev.run("[fib, 2]"), 1)

    def test_3(self):
        self.assertEqual(self.ev.run("[fib, 3]"), 2)

    def test_4(self):
        self.assertEqual(self.ev.run("[fib, 4]"), 3)


class TestDefnWithFib(TestEvaluator):
    def setUp(self):
        super(TestDefnWithFib, self).setUp()
        self.ev.run("""[defn, fib, [x], 
                      [if, [eq, x, 1], 
                            1, 
                      [if, [eq, x, 2], 
                            1, 
                           [+, [fib, [-, x, 1]], [fib, [-, x, 2]]]]]]""")

    def test_1(self):
        self.assertEqual(self.ev.run("[fib, 1]"), 1)

    def test_2(self):
        self.assertEqual(self.ev.run("[fib, 2]"), 1)

    def test_3(self):
        self.assertEqual(self.ev.run("[fib, 3]"), 2)

    def test_4(self):
        self.assertEqual(self.ev.run("[fib, 4]"), 4)


class TestWthLibrary(unittest.TestCase):
    def setUp(self):
        self.ev = Evaluator({})
        self.ev.run("[define, f, [open, common.yaml]]")
        self.ev.run("[define, toload, [read, f]]")
        self.ev.run("[close, f]")
        self.ev.run("[eval, toload]")



if __name__ == '__main__':
    unittest.main()

