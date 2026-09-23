    def _validate_integer(self, key, axis):
        # return a boolean if we have a valid integer indexer

        ax = self.obj._get_axis(axis)
        l = len(ax)
        if key >= l or key < -l:
            raise IndexError("single positional indexer is out-of-bounds")
