    def __setitem__(self, key, val):
        try:
            if key in _deprecated_map:
                version, alt_key, alt_val, inverse_alt = _deprecated_map[key]
                cbook.warn_deprecated(
                    version, name=key, obj_type="rcparam", alternative=alt_key)
                key = alt_key
                val = alt_val(val)
            elif key in _deprecated_remain_as_none and val is not None:
                version, = _deprecated_remain_as_none[key]
                cbook.warn_deprecated(
                    version, name=key, obj_type="rcparam")
            elif key in _deprecated_ignore_map:
                version, alt_key = _deprecated_ignore_map[key]
                cbook.warn_deprecated(
                    version, name=key, obj_type="rcparam", alternative=alt_key)
                return
            elif key == 'examples.directory':
                cbook.warn_deprecated(
                    "3.0", name=key, obj_type="rcparam", addendum="In the "
                    "future, examples will be found relative to the "
                    "'datapath' directory.")
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
                f"{key} is not a valid rc parameter (see rcParams.keys() for "
                f"a list of valid parameters)")
