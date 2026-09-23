    def __setslice__(self, i, j, value):
        if i < 0:
            i = 0
        if j < 0:
            j = 0
        slobj = slice(i, j)  # noqa

        # if not is_scalar(value):
        #    raise Exception("SparseArray does not support setting non-scalars
        # via slices")

        # x = self.values
        # x[slobj] = value
        # self.values = x
        raise TypeError("SparseArray does not support item assignment via "
                        "slices")
