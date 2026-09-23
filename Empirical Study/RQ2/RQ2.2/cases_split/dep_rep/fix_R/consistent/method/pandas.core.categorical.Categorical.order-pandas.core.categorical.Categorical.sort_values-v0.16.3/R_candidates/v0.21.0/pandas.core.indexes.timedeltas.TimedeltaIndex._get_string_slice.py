    def _get_string_slice(self, key, use_lhs=True, use_rhs=True):
        freq = getattr(self, 'freqstr',
                       getattr(self, 'inferred_freq', None))
        if is_integer(key) or is_float(key) or key is NaT:
            self._invalid_indexer('slice', key)
        loc = self._partial_td_slice(key, freq, use_lhs=use_lhs,
                                     use_rhs=use_rhs)
        return loc
