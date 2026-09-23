    def _partial_td_slice(self, key, freq, use_lhs=True, use_rhs=True):

        # given a key, try to figure out a location for a partial slice
        if not isinstance(key, compat.string_types):
            return key

        raise NotImplementedError
