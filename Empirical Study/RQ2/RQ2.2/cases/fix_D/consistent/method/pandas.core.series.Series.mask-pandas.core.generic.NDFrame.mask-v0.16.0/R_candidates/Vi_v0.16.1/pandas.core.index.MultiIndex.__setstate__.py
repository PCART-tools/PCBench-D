    def __setstate__(self, state):
        """Necessary for making this object picklable"""

        if isinstance(state, dict):
            levels = state.get('levels')
            labels = state.get('labels')
            sortorder = state.get('sortorder')
            names = state.get('names')

        elif isinstance(state, tuple):

            nd_state, own_state = state
            levels, labels, sortorder, names = own_state

        self._set_levels([Index(x) for x in levels], validate=False)
        self._set_labels(labels)
        self._set_names(names)
        self.sortorder = sortorder
        self._verify_integrity()
        self._reset_identity()
