    @final
    def _bool_agg(self, val_test: Literal["any", "all"], skipna: bool):
        """
        Shared func to call any / all Cython GroupBy implementations.
        """

        def objs_to_bool(vals: ArrayLike) -> tuple[np.ndarray, type]:
            if is_object_dtype(vals.dtype):
                # GH#37501: don't raise on pd.NA when skipna=True
                if skipna:
                    func = np.vectorize(
                        lambda x: bool(x) if not isna(x) else True, otypes=[bool]
                    )
                    vals = func(vals)
                else:
                    vals = vals.astype(bool, copy=False)

                vals = cast(np.ndarray, vals)
            elif isinstance(vals, BaseMaskedArray):
                vals = vals._data.astype(bool, copy=False)
            else:
                vals = vals.astype(bool, copy=False)

            return vals.view(np.int8), bool

        def result_to_bool(
            result: np.ndarray,
            inference: type,
            nullable: bool = False,
        ) -> ArrayLike:
            if nullable:
                return BooleanArray(result.astype(bool, copy=False), result == -1)
            else:
                return result.astype(inference, copy=False)

        return self._get_cythonized_result(
            libgroupby.group_any_all,
            numeric_only=False,
            cython_dtype=np.dtype(np.int8),
            needs_mask=True,
            needs_nullable=True,
            pre_processing=objs_to_bool,
            post_processing=result_to_bool,
            val_test=val_test,
            skipna=skipna,
        )
