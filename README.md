# cellopype: a reactive pipeline of executable cells

## Introduction

With the cellopype `Cell` and `Pype` classes, you can build a network of **interconnected DataFrames**, each wrapped in its own cell. Each cell has its own 'construction rules' and an update to any cell value is cascaded through the rest of the network.

Think of it as a Jupyter notebook with the cells being automatically (re-)run as required by changes at other points in the notebook. (And without the UI, obviously.)

In abstract terms, a cell consists of a custom `recalc` function that takes a number of inputs (`sources`), and recalculates the cell's `value` from the values of these sources. Any change in value for a given cell is propagated to any other cells depending on it. The network of cells must be one-directional, without any loops (i.e., it has to be a DAG). Lazy computation is default, but subscription-type 'push on change' is supported.

Practically all the work is done by the Cell class, which is relatively small (approx. 50-60 lines). `Pype` is a utility class that adds name spacing logic and convenience methods to a collection of Cells. See below.

## An example with three Cells

![a+b=c](TcBWl.png)

```python
import pandas as pd
from cellopype import Cell
```

```python
# example from https://stackoverflow.com/questions/62671185
dfA = pd.DataFrame([1, 2, 3], columns=["value"])
dfB = pd.DataFrame([10, 20, 30], columns=["value"])

cell_a = Cell(recalc=lambda: dfA.copy())
cell_b = Cell(recalc=lambda: dfB.copy())
```

This is a bit contrived; cell_a and cell_b are 'recalculated' by returning a copy of an external dataframe. We make a copy in order to return a reference to a fresh object instance. Don't have your recalc functions poke around in (or return references to) existing compound objects!

Let's define a recalc function for cell_c and create it:

```python
def plus(a, b):
    return a + b
cell_c = Cell(recalc=plus, sources=[cell_a, cell_b])   # or: recalc=lambda a,b: a+b, sources=[...]
```

Check that cell_a and cell_c are initialized: they are `_dirty`, with no cached `_value` yet:

```python
print('cell_a:', cell_a._dirty, cell_a._value)
cell_a: True None

print('cell_c:', cell_c._dirty, cell_c._value)
cell_c: True None
```

Now comes the nice part. Reading `cell_c.value` triggers recalc of cell_c, which reads cell_a & cell_b values, which in turn triggers recalc of cell_a & cell_b:

```python
print(cell_c.value)

    value
0   11
1   22
2   33
```

Proof of the pudding, change source value for cell_a and recalculate:

```python
dfA.loc[0, "value"] = 222
cell_a.recalc()
```

Reading the value for cell_c again now triggers recalc across the pipeline. \
The row 0 value of cell_c reflects the change in row 0 of cell_a:

```python
print(cell_c.value)

    value
0   232
1   22
2   33
```

## Cell API: summary & example

```python
from cellopype import Cell
```

Every cell must have a **recalc** function that defines how the cell value is (re)calculated from its **sources**:

```python
def recalc_fn( a, b ):
   """Source.values are passed in, returns the new value for this cell"""
   # the values of all its source cells are passed as args to this function
   # args are positional, names do not have to match source names
   return a.add(b)
```

Given the definitions above, we can call the **Cell()** constructor:

```python
my_cell = Cell(
   sources[cell_a, cell_b], # specify the source cells for this cell's recalc
   recalc = recalc_fn,      # calculate new cell.value (source.values as args) [1]
   lazy = True,             # default=True: recalculate only when necessary    [2]
   on_change = plot_it      # optional, called whenever cell 'value' changes   [3]
)
```

1. Our `recalc` function here is pretty trivial. Alternatively, we could simply pass in `recalc=pd.DataFrame.add` \
   (When you pass a class method as recalc function, the first argument is taken as the instance, i.e., _self_.) \

2. If `lazy`=True: the cell's value property is recalculated when: \
   &ensp;&ensp;(1) cell.recalc() is called or \
   &ensp;&ensp;(2) cell.value is read (by your code or by another cell's recalc) and there is no valid cached \_value.\
   If lazy=False, the cell is recalculated immediately when invalidated.

3. `on_change` is called when the cell value changes (comparable to 'subscribe' in RX). The new value is passed as its single argument; no return value is expected. If an on_change handler is supplied, lazy recalculation is disabled.

The cell's **value** property is a getter/setter combo that reads and updates the internal cached `_value`. It can trigger recalc and/or invalidate other cells. A cell value can be a DataFrame, Series or scalar -- but most Python types should work, including lists and dictionaries.

If you want to force recalc for a cell at any time, you can call `my_cell.recalc()` This will only make sense for cells defined with `lazy=True`. In general, you should not have to: reading the output cell values you need should trigger recalc across the network.

Finally, a subtle detail: in `sources` you specify the _cell_ instances that the new cell depends upon (i.e. `cell_a`). The `recalc` function gets passed the _values_ of these cells (i.e., `cell_a.value`). This means your recalc function has no knowledge of or access to the cell. It deals directly with DataFrames or other variables, without having to unwrap them.

## Pype: API summary & example

**Pype** is a helper class to make it easier to manage a network of Cells. A Pype simulates a dictionary with the cell name as key (and with
dot-name access to the attributes). Let's initialize a pype and add some cells to it.

```python
from cellopype import Cell, Pype

pp = Pype()

pp.cell_a = Cell(recalc=lambda: [1,2,3])
pp.cell_b = Cell(recalc=lambda: [4,5,6])

pp.cell_c = Cell(recalc=lambda a, b: a+b, sources=[pp.cell_a, pp.cell_b])
# note that the reference to the source cell instances includes the pype container,
# allowing references to cells in other pypes (or outside of any pype)

pp.keys():
dict_keys(['cell_a', 'cell_b', 'cell_c'])

print(pp.cell_a)
<cellopype.cell.Cell at 0x7fb3100976d0>

print(pp.cell_c.value)
[1, 2, 3, 4, 5, 6]
```

The cell **name** is also added back to the cell:

```python
print(pp.cell_a.name)
'cell_a'    # handy for debugging if a cell can identity itself back to you
```

Pype.**cells** gets all cells in the Pype into a name-based dictionary:

```python
print(pp.cells)
{   'cell_a': <cellopype.cell.Cell object at 0x7fb3100976d0>,
    'cell_b': <cellopype.cell.Cell object at 0x7fb310097790>,
    'cell_c': <cellopype.cell.Cell object at 0x7fb310097910>}
```

Pype.**recalc_all()** forces recalculation of all cells in the Pype.

Pype.**dump_values**() dumps all cell values to a list of dicts while Pype.**load_values**(pld) restores them:

```python
# recalculate and dump all cell values to a list of dicts
pld = pp.dump_values()
print(pld)
[   {'name': 'cell_a', 'value': [1, 2, 3]},
    {'name': 'cell_b', 'value': [4, 5, 6]},
    {'name': 'cell_c', 'value': [1, 2, 3, 4, 5, 6]}]

# ... mess with pp contents
pp.load_values(pld)
# pp values are restored
```

Note these functions only dump and load the _values_. If you want to dump & restore the entire pype, including recalc logic & handlers, use dill to pickle the Pype itself:

```python
import dill  # not pickle, because lambdas

with open('pype_p.dill', 'wb') as file:
    dill.dump(pp, file)
with open('pype_p.dill', 'rb') as inp:
    pp2 = dill.load(inp)
# but heed the warnings: this is not secure unless the dill file is secured;
# and not suitable for structural persistence
```
