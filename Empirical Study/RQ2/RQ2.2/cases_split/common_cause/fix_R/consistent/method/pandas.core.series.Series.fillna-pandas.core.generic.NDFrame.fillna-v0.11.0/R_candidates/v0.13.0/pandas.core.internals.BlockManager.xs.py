    def xs(self, key, axis=1, copy=True, takeable=False):
        if axis < 1:
            raise AssertionError('Can only take xs across axis >= 1, got %d'
                                 % axis)

        # take by position
        if takeable:
            loc = key
        else:
            loc = self.axes[axis].get_loc(key)

        slicer = [slice(None, None) for _ in range(self.ndim)]
        slicer[axis] = loc
        slicer = tuple(slicer)

        new_axes = list(self.axes)

        # could be an array indexer!
        if isinstance(loc, (slice, np.ndarray)):
            new_axes[axis] = new_axes[axis][loc]
        else:
            new_axes.pop(axis)

        new_blocks = []
        if len(self.blocks) > 1:
            if not copy:
                raise Exception('cannot get view of mixed-type or '
                                'non-consolidated DataFrame')
            for blk in self.blocks:
                newb = make_block(blk.values[slicer],
                                  blk.items,
                                  blk.ref_items,
                                  klass=blk.__class__,
                                  fastpath=True)
                new_blocks.append(newb)
        elif len(self.blocks) == 1:
            block = self.blocks[0]
            vals = block.values[slicer]
            if copy:
                vals = vals.copy()
            new_blocks = [make_block(vals,
                                     self.items,
                                     self.items,
                                     klass=block.__class__,
                                     fastpath=True)]

        return self.__class__(new_blocks, new_axes)
