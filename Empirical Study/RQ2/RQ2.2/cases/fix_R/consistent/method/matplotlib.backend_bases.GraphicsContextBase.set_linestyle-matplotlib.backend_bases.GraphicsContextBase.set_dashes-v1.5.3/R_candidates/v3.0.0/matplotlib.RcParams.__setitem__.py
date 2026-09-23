    def __setitem__(self, key, val):
        try:
            if key in _deprecated_map:
                version, alt_key, alt_val, inverse_alt = _deprecated_map[key]
                cbook.warn_deprecated(
                    version, key, obj_type="rcparam", alternative=alt_key)
                key = alt_key
                val = alt_val(val)
            elif key in _deprecated_remain_as_none and val is not None:
                version, = _deprecated_remain_as_none[key]
                addendum = ''
                if key.startswith('backend'):
                    addendum = (
                        "In order to force the use of a specific Qt binding, "
                        "either import that binding first, or set the QT_API "
                        "environment variable.")
                cbook.warn_deprecated(
                    "2.2", name=key, obj_type="rcparam", addendum=addendum)
            elif key in _deprecated_ignore_map:
                version, alt_key = _deprecated_ignore_map[key]
                cbook.warn_deprecated(
                    version, name=key, obj_type="rcparam", alternative=alt_key)
                return
            elif key == 'examples.directory':
                cbook.warn_deprecated(
                    "3.0", "{} is deprecated; in the future, examples will be "
                    "found relative to the 'datapath' directory.".format(key))
            elif key == 'backend':
                if val is rcsetup._auto_backend_sentinel:
                    if 'backend' in self:
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
