    def get_scalar(self, tup):
        """
        Retrieve single item
        """
        full_loc = list(ax.get_loc(x)
                        for ax, x in zip(self.axes, tup))
        blk = self.blocks[self._blknos[full_loc[0]]]
        full_loc[0] = self._blklocs[full_loc[0]]

        # FIXME: this may return non-upcasted types?
        return blk.values[tuple(full_loc)]
