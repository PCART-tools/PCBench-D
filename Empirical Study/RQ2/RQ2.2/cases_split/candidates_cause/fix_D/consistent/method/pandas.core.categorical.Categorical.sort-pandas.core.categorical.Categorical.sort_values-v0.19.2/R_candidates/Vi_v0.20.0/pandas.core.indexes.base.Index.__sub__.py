    def __sub__(self, other):
        raise TypeError("cannot perform __sub__ with this index type: "
                        "{typ}".format(typ=type(self)))
