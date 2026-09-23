    def __setstate__(self, state):
        """Necessary for making this object picklable"""
        if not isinstance(state, dict):
            raise Exception('invalid pickle state')

        # Provide compatibility with pre-0.15.0 Categoricals.
        if '_codes' not in state and 'labels' in state:
            state['_codes'] = state.pop('labels')
        if '_categories' not in state and '_levels' in state:
            state['_categories'] = \
                self._validate_categories(state.pop('_levels'))

        for k, v in compat.iteritems(state):
            setattr(self, k, v)
