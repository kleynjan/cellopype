#!/usr/bin/env python
#
### 'Plotting the End of the Pipeline'

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import sys

sys.path.append("../src")

from cellopype import Cell

# example from https://stackoverflow.com/questions/62671185
### a + b -> c
### if a.value changes, c.on_change plots the (changed) result

fig, ax = plt.subplots(1)
plt.xlim([0, 2])
plt.ylim([0, 50])
ax.xaxis.set_major_locator(MaxNLocator(integer=True))


def myplot(df):  # plot df['value']
    global ax
    if ax.lines:  # updating existing plot
        ax.lines[0].set_xdata(df.index)
        ax.lines[0].set_ydata(df.value)
    else:
        ax.plot(df.index, df, "b")  # 'b': blue
    plt.draw()  # redraws!


dfA = pd.DataFrame([1, 2, 3], columns=["value"])
dfB = pd.DataFrame([10, 20, 30], columns=["value"])
cell_a = Cell(recalc=lambda: dfA)
cell_b = Cell(recalc=lambda: dfB)

pd.DataFrame.add
cell_c = Cell(recalc=pd.DataFrame.add, sources=[cell_a, cell_b], on_change=myplot)
plt.show(block=False)

# plot shows current a+b values
#
input("press enter to change a.value...")
#
# now change cell_a value
#
dfA.loc[0, "value"] = 22
cell_a.invalidate()
#
# -> c.value is changed -> plot changes
#
input("press enter to exit...")
