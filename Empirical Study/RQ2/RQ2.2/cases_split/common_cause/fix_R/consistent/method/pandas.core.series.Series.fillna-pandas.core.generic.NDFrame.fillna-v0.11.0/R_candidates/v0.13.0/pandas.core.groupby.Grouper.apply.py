    def apply(self, f, data, axis=0):
        mutated = False
        splitter = self._get_splitter(data, axis=axis)
        group_keys = self._get_group_keys()

        # oh boy
        if (f.__name__ not in _plotting_methods and
                hasattr(splitter, 'fast_apply') and axis == 0):
            try:
                values, mutated = splitter.fast_apply(f, group_keys)
                return group_keys, values, mutated
            except Exception:
                # we detect a mutation of some kind
                # so take slow path
                pass

        result_values = []
        for key, (i, group) in zip(group_keys, splitter):
            object.__setattr__(group, 'name', key)

            # group might be modified
            group_axes = _get_axes(group)
            res = f(group)
            if not _is_indexed_like(res, group_axes):
                mutated = True
            result_values.append(res)

        return group_keys, result_values, mutated
