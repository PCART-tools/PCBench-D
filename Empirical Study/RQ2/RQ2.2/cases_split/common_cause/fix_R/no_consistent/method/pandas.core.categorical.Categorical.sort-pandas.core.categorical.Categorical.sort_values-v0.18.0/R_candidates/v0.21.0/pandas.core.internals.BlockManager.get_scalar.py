    def get_scalar(self, tup):
        """
        Retrieve single item
        """
        full_loc = list(ax.get_loc(x) for ax, x in zip(self.axes, tup))
        blk = self.blocks[self._blknos[full_loc[0]]]
        values = blk.values

        # FIXME: this may return non-upcasted types?
        if values.ndim == 1:
            return values[full_loc[1]]

        full_loc[0] = self._blklocs[full_loc[0]]
        return values[tuple(full_loc)]
