from .helpers import deep_eq

DEBUG = False


class Cell:
    """Cell class to support reactive dataflow-style dynamic evaluation of DataFrames"""

    def __init__(
        self,
        sources: list = None,
        recalc: callable = None,
        on_change: callable = None,
        lazy: bool = True,
    ):
        """
        Args:
            sources: List of cell instances used to recalc this cell
            recalc: Recalc function; the number of (position-based) arguments to this function must equal len(sources)
            on_change: External function to be called when value changes; cell.value is passed as argument (implies lazy=False)
            lazy: If True (default): do not recalc cell on invalidation but wait for (a) value getter or (b) explicit recalc call
        """
        self.name = ""  # optional, set by Pype
        self.sources = sources or []
        self.recalc_handler = recalc or (lambda *args: None)
        self.on_change_handler = on_change or None
        self.lazy = lazy and not (on_change)
        # init internals:
        self._previous = None
        self._dirty = False
        self._value = None
        self._sinks = []
        for cell in self.sources:
            cell._sinks.append(self)
        self.invalidate()

    def _invalidate_dependents(self):
        for s in self._sinks:
            s.invalidate()

    def invalidate(self):
        if DEBUG and self.name:
            print("%s invalidated" % self.name)
        if self.lazy:
            self._dirty = True
            self._invalidate_dependents()
        else:
            self.recalc()

    @property  # @value.getter
    def value(self):
        if self._dirty:
            self.recalc()
        return self._value

    @value.setter
    def value(self, new_value):
        if DEBUG and self.name:
            print(
                "setting value for %s from %s to %s"
                % (self.name, self._value, new_value)
            )
        self._previous = self._value  # =old _value
        self._value = new_value
        self._dirty = False
        if not deep_eq(self._value, self._previous):
            if DEBUG and self.name:
                print("invalidating dependents for %s" % self.name)
            if self.on_change_handler:
                self.on_change_handler(self.value)
            self._invalidate_dependents()

    def recalc(self):
        # note: calls @value.setter!
        # tip: if the recalc callable is a method, the first arg (=first source.value) is used as 'self'
        new_value = self.recalc_handler(*[src.value for src in self.sources])
        if (
            new_value is not None
        ):  # None is never a valid cell value (eg, invalidated but no recalc function)
            self.value = new_value


CELL_CLASS_NAME = Cell.__name__  # 'Cell', see pype 'cells' property
