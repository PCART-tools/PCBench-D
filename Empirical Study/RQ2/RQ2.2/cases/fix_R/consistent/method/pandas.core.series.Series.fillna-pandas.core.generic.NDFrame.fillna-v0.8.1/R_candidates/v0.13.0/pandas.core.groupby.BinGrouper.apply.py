    def apply(self, f, data, axis=0):
        result_keys = []
        result_values = []
        mutated = False
        for key, group in self.get_iterator(data, axis=axis):
            object.__setattr__(group, 'name', key)

            # group might be modified
            group_axes = _get_axes(group)
            res = f(group)

            if not _is_indexed_like(res, group_axes):
                mutated = True

            result_keys.append(key)
            result_values.append(res)

        return result_keys, result_values, mutated
