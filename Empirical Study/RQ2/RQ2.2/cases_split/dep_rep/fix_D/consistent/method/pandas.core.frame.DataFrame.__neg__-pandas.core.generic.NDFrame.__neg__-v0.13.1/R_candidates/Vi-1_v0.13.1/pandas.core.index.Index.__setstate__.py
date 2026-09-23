    def __setstate__(self, state):
        """Necessary for making this object picklable"""
        if len(state) == 2:
            nd_state, own_state = state
            np.ndarray.__setstate__(self, nd_state)
            self.name = own_state[0]
        else:  # pragma: no cover
            np.ndarray.__setstate__(self, state)
