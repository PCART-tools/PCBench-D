    def __setitem__(self, key, val):
        try:
            if key in _deprecated_map:
                alt_key, alt_val, inverse_alt = _deprecated_map[key]
                warnings.warn(self.msg_depr % (key, alt_key),
                              mplDeprecation)
                key = alt_key
                val = alt_val(val)
            elif key in _deprecated_set and val is not None:
                warnings.warn(self.msg_depr_set % key,
                              mplDeprecation)
            elif key in _deprecated_ignore_map:
                alt = _deprecated_ignore_map[key]
                warnings.warn(self.msg_depr_ignore % (key, alt),
                              mplDeprecation)
                return
            elif key in _obsolete_set:
                warnings.warn(self.msg_obsolete % (key, ),
                              mplDeprecation)
                return
            try:
                cval = self.validate[key](val)
            except ValueError as ve:
                raise ValueError("Key %s: %s" % (key, str(ve)))
            dict.__setitem__(self, key, cval)
        except KeyError:
            raise KeyError(
                '%s is not a valid rc parameter. See rcParams.keys() for a '
                'list of valid parameters.' % (key,))
