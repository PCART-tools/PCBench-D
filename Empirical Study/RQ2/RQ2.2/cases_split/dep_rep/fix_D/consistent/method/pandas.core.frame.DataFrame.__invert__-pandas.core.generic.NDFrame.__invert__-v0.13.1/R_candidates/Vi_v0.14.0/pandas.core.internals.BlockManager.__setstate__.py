    def __setstate__(self, state):
        # discard anything after 3rd, support beta pickling format for a little
        # while longer
        ax_arrays, bvalues, bitems = state[:3]

        self.axes = [_ensure_index(ax) for ax in ax_arrays]

        blocks = []
        for values, items in zip(bvalues, bitems):

            # numpy < 1.7 pickle compat
            if values.dtype == 'M8[us]':
                values = values.astype('M8[ns]')

            blk = make_block(values,
                             placement=self.axes[0].get_indexer(items))
            blocks.append(blk)
        self.blocks = tuple(blocks)

        self._post_setstate()
