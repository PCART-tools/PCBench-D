    def split_block_at(self, item):
        """
        Split block into zero or more blocks around columns with given label,
        for "deleting" a column without having to copy data by returning views
        on the original array.

        Returns
        -------
        generator of Block
        """
        loc = self.items.get_loc(item)

        if type(loc) == slice or type(loc) == int:
            mask = [True] * len(self)
            mask[loc] = False
        else:  # already a mask, inverted
            mask = -loc

        for s, e in com.split_ranges(mask):
            yield make_block(self.values[s:e],
                             self.items[s:e].copy(),
                             self.ref_items,
                             ndim=self.ndim,
                             klass=self.__class__,
                             fastpath=True)
