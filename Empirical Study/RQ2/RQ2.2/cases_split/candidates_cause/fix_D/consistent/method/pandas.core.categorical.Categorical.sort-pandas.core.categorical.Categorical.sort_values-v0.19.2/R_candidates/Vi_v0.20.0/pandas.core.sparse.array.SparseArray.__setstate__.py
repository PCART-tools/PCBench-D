    def __setstate__(self, state):
        """Necessary for making this object picklable"""
        nd_state, own_state = state
        np.ndarray.__setstate__(self, nd_state)

        fill_value, sp_index = own_state[:2]
        self.sp_index = sp_index
        self._fill_value = fill_value
