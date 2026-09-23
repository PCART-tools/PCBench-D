    def get_scalar(self, tup):
        """
        Retrieve single item
        """
        item = tup[0]
        _, blk = self._find_block(item)

        # this could obviously be seriously sped up in cython
        item_loc = blk.items.get_loc(item),
        full_loc = item_loc + tuple(ax.get_loc(x)
                                    for ax, x in zip(self.axes[1:], tup[1:]))
        return blk.values[full_loc]
