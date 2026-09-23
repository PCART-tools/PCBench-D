    def _bool_agg(self, val_test, skipna):
        """
        Shared func to call any / all Cython GroupBy implementations.
        """

        def objs_to_bool(vals: np.ndarray) -> Tuple[np.ndarray, Type]:
            if is_object_dtype(vals):
                vals = np.array([bool(x) for x in vals])
            else:
                vals = vals.astype(np.bool)

            return vals.view(np.uint8), np.bool

        def result_to_bool(result: np.ndarray, inference: Type) -> np.ndarray:
            return result.astype(inference, copy=False)

        return self._get_cythonized_result(
            "group_any_all",
            aggregate=True,
            cython_dtype=np.dtype(np.uint8),
            needs_values=True,
            needs_mask=True,
            pre_processing=objs_to_bool,
            post_processing=result_to_bool,
            val_test=val_test,
            skipna=skipna,
        )
