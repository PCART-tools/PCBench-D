    def _cython_transform(
        self,
        how: str,
        numeric_only: bool = False,
        axis: AxisInt = 0,
        **kwargs,
    ) -> DataFrame:
        assert axis == 0  # handled by caller

        # With self.axis == 0, we have multi-block tests
        #  e.g. test_rank_min_int, test_cython_transform_frame
        #  test_transform_numeric_ret
        # With self.axis == 1, _get_data_to_aggregate does a transpose
        #  so we always have a single block.
        mgr: Manager2D = self._get_data_to_aggregate(
            numeric_only=numeric_only, name=how
        )

        def arr_func(bvalues: ArrayLike) -> ArrayLike:
            return self.grouper._cython_operation(
                "transform", bvalues, how, 1, **kwargs
            )

        # We could use `mgr.apply` here and not have to set_axis, but
        #  we would have to do shape gymnastics for ArrayManager compat
        res_mgr = mgr.grouped_reduce(arr_func)
        res_mgr.set_axis(1, mgr.axes[1])

        res_df = self.obj._constructor_from_mgr(res_mgr, axes=res_mgr.axes)
        res_df = self._maybe_transpose_result(res_df)
        return res_df
