    def _aggregate_series_pure_python(self, obj, func):

        group_index, _, ngroups = self.group_info

        counts = np.zeros(ngroups, dtype=int)
        result = None

        splitter = get_splitter(obj, group_index, ngroups, axis=self.axis)

        for label, group in splitter:
            res = func(group)
            if result is None:
                if (isinstance(res, (Series, Index, np.ndarray))):
                    raise ValueError('Function does not reduce')
                result = np.empty(ngroups, dtype='O')

            counts[label] = group.shape[0]
            result[label] = res

        result = lib.maybe_convert_objects(result, try_float=0)
        return result, counts
