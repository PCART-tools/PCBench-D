    @final
    def _pad_or_backfill(
        self,
        method: Literal["ffill", "bfill", "pad", "backfill"],
        *,
        axis: None | Axis = None,
        inplace: bool_t = False,
        limit: None | int = None,
        downcast: dict | None = None,
    ):
        if axis is None:
            axis = 0
        axis = self._get_axis_number(axis)
        method = clean_fill_method(method)

        if not self._mgr.is_single_block and axis == 1:
            if inplace:
                raise NotImplementedError()
            result = self.T._pad_or_backfill(method=method, limit=limit).T

            return result

        new_mgr = self._mgr.pad_or_backfill(
            method=method,
            axis=self._get_block_manager_axis(axis),
            limit=limit,
            inplace=inplace,
            downcast=downcast,
        )
        result = self._constructor_from_mgr(new_mgr, axes=new_mgr.axes)
        if inplace:
            return self._update_inplace(result)
        else:
            return result.__finalize__(self, method="fillna")
