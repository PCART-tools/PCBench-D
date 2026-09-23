    def __setstate__(self, state):
        # discard anything after 3rd, support beta pickling format for a little
        # while longer
        ax_arrays, bvalues, bitems = state[:3]

        self.axes = [_ensure_index(ax) for ax in ax_arrays]
        self.axes = _handle_legacy_indexes(self.axes)

        blocks = []
        for values, items in zip(bvalues, bitems):

            # numpy < 1.7 pickle compat
            if values.dtype == 'M8[us]':
                values = values.astype('M8[ns]')

            blk = make_block(values, items, self.axes[0])
            blocks.append(blk)
        self.blocks = blocks

        self._post_setstate()
