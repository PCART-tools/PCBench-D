    def _bool_agg(self, val_test, skipna):
        """Shared func to call any / all Cython GroupBy implementations"""

        def objs_to_bool(vals):
            try:
                vals = vals.astype(np.bool)
            except ValueError:  # for objects
                vals = np.array([bool(x) for x in vals])

            return vals.view(np.uint8)

        def result_to_bool(result):
            return result.astype(np.bool, copy=False)

        return self._get_cythonized_result('group_any_all', self.grouper,
                                           aggregate=True,
                                           cython_dtype=np.uint8,
                                           needs_values=True,
                                           needs_mask=True,
                                           pre_processing=objs_to_bool,
                                           post_processing=result_to_bool,
                                           val_test=val_test, skipna=skipna)
