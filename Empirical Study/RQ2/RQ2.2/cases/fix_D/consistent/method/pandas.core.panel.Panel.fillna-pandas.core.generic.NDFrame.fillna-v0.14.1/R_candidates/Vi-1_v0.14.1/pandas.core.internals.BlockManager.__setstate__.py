    def __setstate__(self, state):
        def unpickle_block(values, mgr_locs):
            # numpy < 1.7 pickle compat
            if values.dtype == 'M8[us]':
                values = values.astype('M8[ns]')
            return make_block(values, placement=mgr_locs)

        if (isinstance(state, tuple) and len(state) >= 4
            and '0.14.1' in state[3]):
            state = state[3]['0.14.1']
            self.axes = [_ensure_index(ax) for ax in state['axes']]
            self.blocks = tuple(
                unpickle_block(b['values'], b['mgr_locs'])
                for b in state['blocks'])
        else:
            # discard anything after 3rd, support beta pickling format for a
            # little while longer
            ax_arrays, bvalues, bitems = state[:3]

            self.axes = [_ensure_index(ax) for ax in ax_arrays]
            self.blocks = tuple(
                unpickle_block(values,
                               self.axes[0].get_indexer(items))
                for values, items in zip(bvalues, bitems))

        self._post_setstate()
