    @final
    def __pos__(self) -> Self:
        def blk_func(values: ArrayLike):
            if is_bool_dtype(values.dtype):
                return values.copy()
            else:
                # error: Argument 1 to "pos" has incompatible type "Union
                # [ExtensionArray, ndarray[Any, Any]]"; expected
                # "_SupportsPos[ndarray[Any, dtype[Any]]]"
                return operator.pos(values)  # type: ignore[arg-type]

        new_data = self._mgr.apply(blk_func)
        res = self._constructor_from_mgr(new_data, axes=new_data.axes)
        return res.__finalize__(self, method="__pos__")
