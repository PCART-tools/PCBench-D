    def __setstate__(self, state):
        """Necessary for making this object picklable"""
        if not isinstance(state, dict):
            raise Exception('invalid pickle state')

        # Provide compatibility with pre-0.15.0 Categoricals.
        if '_categories' not in state and '_levels' in state:
            state['_categories'] = self.dtype.validate_categories(state.pop(
                '_levels'))
        if '_codes' not in state and 'labels' in state:
            state['_codes'] = coerce_indexer_dtype(
                state.pop('labels'), state['_categories'])

        # 0.16.0 ordered change
        if '_ordered' not in state:

            # >=15.0 < 0.16.0
            if 'ordered' in state:
                state['_ordered'] = state.pop('ordered')
            else:
                state['_ordered'] = False

        # 0.21.0 CategoricalDtype change
        if '_dtype' not in state:
            state['_dtype'] = CategoricalDtype(state['_categories'],
                                               state['_ordered'])

        for k, v in compat.iteritems(state):
            setattr(self, k, v)
