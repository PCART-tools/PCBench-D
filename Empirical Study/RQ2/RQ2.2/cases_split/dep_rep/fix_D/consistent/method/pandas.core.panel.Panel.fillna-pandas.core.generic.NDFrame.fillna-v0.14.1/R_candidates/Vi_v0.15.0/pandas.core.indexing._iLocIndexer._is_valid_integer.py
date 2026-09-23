    def _is_valid_integer(self, key, axis):
        # return a boolean if we have a valid integer indexer

        ax = self.obj._get_axis(axis)
        if key > len(ax):
            raise IndexError("single positional indexer is out-of-bounds")
        return True
