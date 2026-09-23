    def __getitem__(self, key):
        inverse_alt = None
        if key in _deprecated_map:
            alt_key, alt_val, inverse_alt = _deprecated_map[key]
            warnings.warn(self.msg_depr % (key, alt_key),
                          mplDeprecation)
            key = alt_key

        elif key in _deprecated_ignore_map:
            alt = _deprecated_ignore_map[key]
            warnings.warn(self.msg_depr_ignore % (key, alt),
                          mplDeprecation)
            key = alt

        elif key in _obsolete_set:
            warnings.warn(self.msg_obsolete % (key, ),
                          mplDeprecation)
            return None

        val = dict.__getitem__(self, key)
        if inverse_alt is not None:
            return inverse_alt(val)
        else:
            return val
