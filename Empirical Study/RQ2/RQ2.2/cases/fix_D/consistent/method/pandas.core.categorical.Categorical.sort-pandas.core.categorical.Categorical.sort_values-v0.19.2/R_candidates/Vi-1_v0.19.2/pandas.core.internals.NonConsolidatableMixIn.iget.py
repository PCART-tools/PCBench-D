    def iget(self, col):

        if self.ndim == 2 and isinstance(col, tuple):
            col, loc = col
            if not is_null_slice(col) and col != 0:
                raise IndexError("{0} only contains one item".format(self))
            return self.values[loc]
        else:
            if col != 0:
                raise IndexError("{0} only contains one item".format(self))
            return self.values
