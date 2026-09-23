    def __setstate__(self, state):
        """Necessary for making this object picklable"""
        nd_state, own_state = state
        np.ndarray.__setstate__(self, nd_state)
        levels, labels, sortorder, names = own_state

        self._set_levels([Index(x) for x in levels], validate=False)
        self._set_labels(labels)
        self._set_names(names)
        self.sortorder = sortorder
        self._verify_integrity()
