    def __setstate__(self, state):
        """Necessary for making this object picklable"""
        if not isinstance(state, dict):
            raise Exception('invalid pickle state')

        # Provide compatibility with pre-0.15.0 Categoricals.
        if '_categories' not in state and '_levels' in state:
            state['_categories'] = self._validate_categories(state.pop(
                '_levels'))
        if '_codes' not in state and 'labels' in state:
            state['_codes'] = _coerce_indexer_dtype(state.pop('labels'),
                                                    state['_categories'])

        # 0.16.0 ordered change
        if '_ordered' not in state:

            # >=15.0 < 0.16.0
            if 'ordered' in state:
                state['_ordered'] = state.pop('ordered')
            else:
                state['_ordered'] = False

        for k, v in compat.iteritems(state):
            setattr(self, k, v)
