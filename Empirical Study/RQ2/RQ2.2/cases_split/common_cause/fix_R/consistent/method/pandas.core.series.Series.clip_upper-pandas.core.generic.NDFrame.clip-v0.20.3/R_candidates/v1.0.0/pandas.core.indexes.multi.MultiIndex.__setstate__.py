    def __setstate__(self, state):
        """Necessary for making this object picklable"""

        if isinstance(state, dict):
            levels = state.get("levels")
            codes = state.get("codes")
            sortorder = state.get("sortorder")
            names = state.get("names")

        elif isinstance(state, tuple):

            nd_state, own_state = state
            levels, codes, sortorder, names = own_state

        self._set_levels([Index(x) for x in levels], validate=False)
        self._set_codes(codes)
        new_codes = self._verify_integrity()
        self._set_codes(new_codes)
        self._set_names(names)
        self.sortorder = sortorder
        self._reset_identity()
