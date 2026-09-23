    def __setitem__(self, key, val):
        try:
            if key in _deprecated_map:
                version, alt_key, alt_val, inverse_alt = _deprecated_map[key]
                _api.warn_deprecated(
                    version, name=key, obj_type="rcparam", alternative=alt_key)
                key = alt_key
                val = alt_val(val)
            elif key in _deprecated_remain_as_none and val is not None:
                version, = _deprecated_remain_as_none[key]
                _api.warn_deprecated(version, name=key, obj_type="rcparam")
            elif key in _deprecated_ignore_map:
                version, alt_key = _deprecated_ignore_map[key]
                _api.warn_deprecated(
                    version, name=key, obj_type="rcparam", alternative=alt_key)
                return
            elif key == 'backend':
                if val is rcsetup._auto_backend_sentinel:
                    if 'backend' in self:
                        return
            try:
                cval = self.validate[key](val)
            except ValueError as ve:
                raise ValueError(f"Key {key}: {ve}") from None
            dict.__setitem__(self, key, cval)
        except KeyError as err:
            raise KeyError(
                f"{key} is not a valid rc parameter (see rcParams.keys() for "
                f"a list of valid parameters)") from err
