from .cell import CELL_CLASS_NAME


class Pype(dict):
    """A dict-like collection of Cells"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.__dict__.update({key: value})
        if type(self[key]).__name__ == CELL_CLASS_NAME:
            self[key].name = key

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    @property
    def cells(self):
        """Returns dict {cell_name: cell_instance} for every cell in this pype"""
        return {
            k: v for k, v in self.items() if type(v).__name__ == CELL_CLASS_NAME
        }

    def recalc_all(self):
        """Recalc all cells in this pype"""
        for cell in self.cells.values():
            cell.recalc()

    def dump_values(self):
        """Return all recalculated cell values in a list of dicts [{'name': ..., 'value': ...}]"""
        self.recalc_all()
        return [
            {
                "name": key,
                "value": cell._value.copy()
                if "pandas" in str(type(cell._value))
                else cell._value,
            }
            for key, cell in self.cells.items()
        ]

    def load_values(self, name_value_list):
        """Restore cell values from a list of dicts [{'name': ..., 'value': ...}]"""
        for item in name_value_list:
            self[item["name"]]._value = item["value"]
            self[item["name"]]._dirty = False

    ## in order to load/dump entire Pypes, including dependencies and recalc functions, consider dill:
    ## given a 'pype' collection with cells:
    #
    # import dill
    #
    # with open('pype_p.dill', 'wb') as outp:
    #    dill.dump(pype, outp)
    # with open('pype_p.dill', 'rb') as inp:
    #    pype_2 = dill.load(inp)
    #
    ## note 1. security concerns: code injectable by anyone with acess to dill file
    ##      2. fragile to lib versions: do not use as a structural persistance mechanism
