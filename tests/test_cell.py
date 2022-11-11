## how to run unit tests (bloody ridiculous, this)
# $ cd ../src
# $ python -m unittest discover ../tests

import unittest

from cellopype import Cell


class Tests(unittest.TestCase):
    def test_naked_init(self):
        self.c1 = Cell()
        self.assertEqual(self.c1._dirty, True)
        self.assertEqual(self.c1._value, None)
        self.assertEqual(self.c1.recalc_handler(), None)
        self.assertEqual(self.c1.on_change_handler, None)

    def test_init_with_value(self):
        self.test_naked_init()
        self.c1.value = 1
        self.assertEqual(self.c1._value, 1)
        self.assertEqual(self.c1._dirty, False)

    def test_init_with_lazy_recalc(self):
        def my_recalc(x):
            return x * 2

        self.test_init_with_value()  # get c1==1
        self.c2 = Cell(recalc=my_recalc, sources=[self.c1])
        self.c3 = Cell(recalc=my_recalc, sources=[self.c2])
        self.assertEqual(self.c2._value, None)
        self.assertEqual(self.c3._value, None)
        self.c1.invalidate()
        self.assertEqual(self.c2._value, None)
        dummy = self.c3.value
        self.assertEqual(dummy, 4)
        self.assertEqual(self.c2._value, 2)

    def test_init_with_immediate_recalc(self):
        def my_recalc(x):
            return x * 2

        self.test_init_with_value()  # get c1==1
        self.c2 = Cell(recalc=my_recalc, sources=[self.c1], lazy=False)
        self.c3 = Cell(recalc=my_recalc, sources=[self.c2], lazy=False)
        self.assertEqual(self.c2._value, 2)
        self.assertEqual(self.c3._value, 4)

    def test_init_with_onchange_recalc(self):
        self.testvar = None

        def my_recalc(x):
            return x * 2

        def my_on_change(x):
            self.testvar = x

        self.test_init_with_value()  # get c1==1
        self.assertEqual(self.c1._value, 1)
        self.c2 = Cell(recalc=my_recalc, sources=[self.c1], lazy=True)
        self.assertEqual(self.c2._value, None)

        self.c3 = Cell(recalc=my_recalc, sources=[self.c2], on_change=my_on_change)
        # recalc c3 is forced straight away -> triggering c2 recalc
        self.assertEqual(self.c2._value, 2)
        self.assertEqual(self.c3._value, 4)
        self.assertEqual(self.testvar, 4)

    def test_onchange_pipeline(self):
        self.test_init_with_onchange_recalc()
        self.c1.value = 3
        self.assertEqual(self.testvar, 12)  # 3*2*2, set through on_change


if __name__ == "__main__":
    unittest.main()
