# the shortest & sweetest...
# a. no setters, so explictly call recalc on the cell if the value changes
# b. always evaluates; no lazy logic

from .helpers import deep_eq


class MinimalCell:
    def __init__(
        self,
        sources: list = None,
        recalc: callable = None,
        on_change: callable = None,
    ):
        self.sources = sources or []  # list of cells
        self.recalc_handler = recalc or (lambda *args: None)
        self.on_change_handler = on_change or (lambda *args: None)
        self._previous = None
        self.sinks = []
        for cell in self.sources:
            cell.sinks.append(self)
        self.recalc()

    def recalc(self):
        self._previous = self.value
        self.value = self.recalc_handler(*[src.value for src in self.sources])
        if not deep_eq(self.value, self._previous):
            self.on_change_handler(self.value)
            for s in self.sinks:
                s.recalc()
