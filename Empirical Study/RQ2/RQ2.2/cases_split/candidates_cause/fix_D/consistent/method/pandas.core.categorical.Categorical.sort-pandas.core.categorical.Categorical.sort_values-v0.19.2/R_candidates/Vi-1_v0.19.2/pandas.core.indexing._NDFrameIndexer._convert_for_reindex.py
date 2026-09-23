    def _convert_for_reindex(self, key, axis=0):
        labels = self.obj._get_axis(axis)

        if is_bool_indexer(key):
            key = check_bool_indexer(labels, key)
            return labels[key]
        else:
            if isinstance(key, Index):
                # want Index objects to pass through untouched
                keyarr = key
            else:
                # asarray can be unsafe, NumPy strings are weird
                keyarr = _asarray_tuplesafe(key)

            if is_integer_dtype(keyarr) and not labels.is_integer():
                keyarr = _ensure_platform_int(keyarr)
                return labels.take(keyarr)

            return keyarr
