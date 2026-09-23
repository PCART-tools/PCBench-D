    def _apply(
        self,
        func: Callable[..., Styler],
        axis: Axis | None = 0,
        subset: Subset | None = None,
        **kwargs,
    ) -> Styler:
        subset = slice(None) if subset is None else subset
        subset = non_reducing_slice(subset)
        data = self.data.loc[subset]
        if axis is not None:
            result = data.apply(func, axis=axis, result_type="expand", **kwargs)
            result.columns = data.columns
        else:
            result = func(data, **kwargs)
            if not isinstance(result, DataFrame):
                if not isinstance(result, np.ndarray):
                    raise TypeError(
                        f"Function {repr(func)} must return a DataFrame or ndarray "
                        f"when passed to `Styler.apply` with axis=None"
                    )
                if not (data.shape == result.shape):
                    raise ValueError(
                        f"Function {repr(func)} returned ndarray with wrong shape.\n"
                        f"Result has shape: {result.shape}\n"
                        f"Expected shape: {data.shape}"
                    )
                result = DataFrame(result, index=data.index, columns=data.columns)
            elif not (
                result.index.equals(data.index) and result.columns.equals(data.columns)
            ):
                raise ValueError(
                    f"Result of {repr(func)} must have identical "
                    f"index and columns as the input"
                )

        if result.shape != data.shape:
            raise ValueError(
                f"Function {repr(func)} returned the wrong shape.\n"
                f"Result has shape: {result.shape}\n"
                f"Expected shape:   {data.shape}"
            )
        self._update_ctx(result)
        return self
