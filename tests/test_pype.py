## how to run unit tests (bloody ridiculous, this)
# $ cd ../src
# $ python -m unittest discover ../tests

import unittest
import json

from cellopype import Cell, Pype


class PypeTests(unittest.TestCase):
    def setUp(self):
        self.pp = Pype()
        self.pp.c1 = Cell(recalc=lambda: 1)
        self.pp.c1.value = 1
        self.pp.c2 = Cell(recalc=lambda: 2)
        self.pp.c2.value = 2
        self.pp.c2._value = 2
        self.pp.c2.lazy = True
        self.assertEqual(self.pp.c1.name, "c1")
        self.assertEqual(self.pp.c1.value, 1)

    def test_dump_values(self):
        # self.make_pype_with_cells()
        self.assertEqual(self.pp.c1.value, 1)
        cell_dict = self.pp.cells
        self.assertEqual(cell_dict["c1"].value, 1)
        self.assertEqual(cell_dict["c1"]._value, 1)
        # json_list = json.dumps(self.pp.dump_values())
        # lits = json.loads(json_list)
        lits = self.pp.dump_values()
        self.assertEqual(len(lits), 2)
        self.assertEqual(lits[0]["name"], "c1")
        self.assertEqual(lits[1]["value"], 2)

    def test_load_values(self):
        # self.make_pype_with_cells()
        lits = self.pp.dump_values()
        self.pp.c1._value = 111
        self.pp.c1.value = 111
        self.pp.c2._value = 222
        self.pp.c2.value = 222
        self.pp.load_values(lits)
        self.assertEqual(self.pp.c1._value, 1)
        self.assertEqual(self.pp.c2._value, 2)
        self.assertEqual(self.pp.c1._dirty, False)
        self.assertEqual(self.pp.c2._dirty, False)

    def test_force_recalc(self):
        self.ppp = Pype(force_unlazy=True)
        self.ppp.c1 = Cell(recalc=lambda: 1)
        self.ppp.c1.value = 1

        def my_recalc(x):
            return x * 2

        self.ppp.c2 = Cell(recalc=my_recalc, sources=[self.ppp.c1])
        self.ppp.c3 = Cell(recalc=my_recalc, sources=[self.ppp.c2])
        self.assertEqual(self.ppp.c2.lazy, False)
        self.ppp.c1.value = 2
        self.assertEqual(self.ppp.c2._value, 4)
        self.assertEqual(self.ppp.c3._value, 8)

    # def dump_values(self):
    #    """Return all recalculated cell values in a list of dicts [{'name': ..., 'value': ...}]"""
    #    self.recalc_all()
    #    return [
    #        {"name": key, "value": cell._value} for key, cell in self.cells.items()
    #    ]


if __name__ == "__main__":
    unittest.main()
