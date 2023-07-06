from unittest import TestCase
from auto_swap import *


class Test(TestCase):
    def test_simple(self):
        for c in "=+-*/,:":
            self.assertEqual(auto_swap("a" + c + "b"), "b" + c + "a")
            self.assertEqual(auto_swap("aa" + c + "b"), "b" + c + "aa")
            self.assertEqual(auto_swap("a " + c + " b"), "b " + c + " a")
            self.assertEqual(auto_swap("a    " + c + "b"), "b    " + c + "a")
        self.assertEqual(auto_swap("a.b, x"), "x, a.b")

    def test_multiple_central_symbols(self):
        self.assertRaises(MultipleCentralSymbols, auto_swap, "a=b=c")
        self.assertRaises(MultipleCentralSymbols, auto_swap, "a-b+c")

    def test_no_central_symbol(self):
        self.assertRaises(NoCentralSymbols, auto_swap, "abc")
        self.assertRaises(NoCentralSymbols, auto_swap, "{}()[]")

    def test_nested_simple(self):
        self.assertEqual(auto_swap("foo(a, b) + bar(x, y)"), "bar(x, y) + foo(a, b)")
        self.assertEqual(auto_swap("foo[a * b] + bar{x - y}"), "bar{x - y} + foo[a * b]")

    def test_strings(self):
        self.assertEqual(auto_swap("'a, b' + \"x, y\""), "\"x, y\" + 'a, b'")
        self.assertEqual(auto_swap("'foo[a * b]' + \"bar{x - y}\""), "\"bar{x - y}\" + 'foo[a * b]'")
        self.assertEqual(auto_swap('openings = "([{"'), '"([{" = openings')

    def test_missing_closing(self):
        self.assertRaises(MissingClosing, auto_swap, "foo(a, b")
        self.assertRaises(MissingClosing, auto_swap, "foo[a + b")
        self.assertRaises(MissingClosing, auto_swap, "foo{a / b")
        self.assertRaises(MissingClosing, auto_swap, "bar(foo(a, b)")

    def test_missing_opening(self):
        self.assertRaises(MissingOpening, auto_swap, "foo a, b)")
        self.assertRaises(MissingOpening, auto_swap, "bar(foo(a + b))}")

    def test_string_not_closed(self):
        self.assertRaises(MissingClosing, auto_swap, "'a, b")
        self.assertRaises(MissingClosing, auto_swap, "'\"a, b\"")

    def test0(self):
        self.assertEqual(auto_swap('result, "adj.&cn. required, necessary."'), '"adj.&cn. required, necessary.", result')