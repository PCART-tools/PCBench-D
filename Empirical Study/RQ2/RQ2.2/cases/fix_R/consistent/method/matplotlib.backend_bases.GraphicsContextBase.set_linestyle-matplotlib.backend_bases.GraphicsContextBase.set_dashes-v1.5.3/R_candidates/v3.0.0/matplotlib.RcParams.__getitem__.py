    def __getitem__(self, key):
        if key in _deprecated_map:
            version, alt_key, alt_val, inverse_alt = _deprecated_map[key]
            cbook.warn_deprecated(
                version, key, obj_type="rcparam", alternative=alt_key)
            return inverse_alt(dict.__getitem__(self, alt_key))

        elif key in _deprecated_ignore_map:
            version, alt_key = _deprecated_ignore_map[key]
            cbook.warn_deprecated(
                version, key, obj_type="rcparam", alternative=alt_key)
            return dict.__getitem__(self, alt_key) if alt_key else None

        elif key == 'examples.directory':
            cbook.warn_deprecated(
                "3.0", "{} is deprecated; in the future, examples will be "
                "found relative to the 'datapath' directory.".format(key))

        elif key == "backend":
            val = dict.__getitem__(self, key)
            if val is rcsetup._auto_backend_sentinel:
                from matplotlib import pyplot as plt
                plt.switch_backend(rcsetup._auto_backend_sentinel)

        return dict.__getitem__(self, key)
