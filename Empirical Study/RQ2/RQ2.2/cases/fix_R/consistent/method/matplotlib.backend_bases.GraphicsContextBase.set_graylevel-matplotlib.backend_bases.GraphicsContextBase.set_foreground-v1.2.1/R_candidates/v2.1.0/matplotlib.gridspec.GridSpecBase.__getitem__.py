    def __getitem__(self, key):
        """
        create and return a SuplotSpec instance.
        """
        nrows, ncols = self.get_geometry()
        total = nrows*ncols

        if isinstance(key, tuple):
            try:
                k1, k2 = key
            except ValueError:
                raise ValueError("unrecognized subplot spec")

            if isinstance(k1, slice):
                row1, row2, _ = k1.indices(nrows)
            else:
                if k1 < 0:
                    k1 += nrows
                if k1 >= nrows or k1 < 0 :
                    raise IndexError("index out of range")
                row1, row2 = k1, k1+1

            if isinstance(k2, slice):
                col1, col2, _ = k2.indices(ncols)
            else:
                if k2 < 0:
                    k2 += ncols
                if k2 >= ncols or k2 < 0 :
                    raise IndexError("index out of range")
                col1, col2 = k2, k2+1

            num1 = row1*ncols + col1
            num2 = (row2-1)*ncols + (col2-1)

        # single key
        else:
            if isinstance(key, slice):
                num1, num2, _ = key.indices(total)
                num2 -= 1
            else:
                if key < 0:
                    key += total
                if key >= total or key < 0 :
                    raise IndexError("index out of range")
                num1, num2 = key, None

        return SubplotSpec(self, num1, num2)
