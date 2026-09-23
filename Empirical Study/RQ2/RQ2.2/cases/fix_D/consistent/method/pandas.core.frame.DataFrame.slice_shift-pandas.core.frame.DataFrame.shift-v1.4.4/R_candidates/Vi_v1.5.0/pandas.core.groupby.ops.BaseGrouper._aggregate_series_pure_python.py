    @final
    def _aggregate_series_pure_python(
        self, obj: Series, func: Callable
    ) -> npt.NDArray[np.object_]:
        ids, _, ngroups = self.group_info

        counts = np.zeros(ngroups, dtype=int)
        result = np.empty(ngroups, dtype="O")
        initialized = False

        # equiv: splitter = self._get_splitter(obj, axis=0)
        splitter = get_splitter(obj, ids, ngroups, axis=0)

        for i, group in enumerate(splitter):
            res = func(group)
            res = libreduction.extract_result(res)

            if not initialized:
                # We only do this validation on the first iteration
                libreduction.check_result_array(res, group.dtype)
                initialized = True

            counts[i] = group.shape[0]
            result[i] = res

        return result
