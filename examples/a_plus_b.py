#!/usr/bin/env python
import sys

sys.path.append("../src")

import pandas as pd
from cellopype import Cell

# example from https://stackoverflow.com/questions/62671185
dfA = pd.DataFrame([1, 2, 3], columns=["value"])
dfB = pd.DataFrame([10, 20, 30], columns=["value"])
cell_a = Cell(recalc=lambda: dfA)
cell_b = Cell(recalc=lambda: dfB)

# def recalc_fn(a, b):
#    return pd.DataFrame(a + b)
# cell_c = Cell(recalc=recalc_fn, sources=[cell_a, cell_b])
## or more succinct:
cell_c = Cell(recalc=pd.DataFrame.add, sources=[cell_a, cell_b])

print("\nShowing lazy evaluation (default):")
print("\ncell_a internal value is not yet calculated:")
print(cell_a._value)
print("\nReading c.value -> recalc c -> recalc a & b")
print(cell_c.value)
print("\ncell_a now has an internal value:")
print(cell_a._value)
print("\n\nChange source value in dfA and invalidate cell_a:")
dfA.loc[0, "value"] = 222
print(dfA)
cell_a.invalidate()  # or cell_a.recalc(), or cell_a.value=dfA
print("\nNow calculate cell_c again:")
print(cell_c.value)
