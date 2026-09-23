    def _get_partial_string_timestamp_match_key(self, key, labels):
        """Translate any partial string timestamp matches in key, returning the
        new key (GH 10331)"""
        if isinstance(labels, MultiIndex):
            if isinstance(key, compat.string_types) and \
                    labels.levels[0].is_all_dates:
                # Convert key '2016-01-01' to
                # ('2016-01-01'[, slice(None, None, None)]+)
                key = tuple([key] + [slice(None)] * (len(labels.levels) - 1))

            if isinstance(key, tuple):
                # Convert (..., '2016-01-01', ...) in tuple to
                # (..., slice('2016-01-01', '2016-01-01', None), ...)
                new_key = []
                for i, component in enumerate(key):
                    if isinstance(component, compat.string_types) and \
                            labels.levels[i].is_all_dates:
                        new_key.append(slice(component, component, None))
                    else:
                        new_key.append(component)
                key = tuple(new_key)

        return key
