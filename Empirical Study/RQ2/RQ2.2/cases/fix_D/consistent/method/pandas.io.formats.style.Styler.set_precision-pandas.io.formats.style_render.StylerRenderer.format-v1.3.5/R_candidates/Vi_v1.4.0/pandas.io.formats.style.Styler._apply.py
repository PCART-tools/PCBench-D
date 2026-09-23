    def _apply(
        self,
        func: Callable,
        axis: Axis | None = 0,
        subset: Subset | None = None,
        **kwargs,
    ) -> Styler:
        subset = slice(None) if subset is None else subset
        subset = non_reducing_slice(subset)
        data = self.data.loc[subset]
        if axis is None:
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
        else:
            axis = self.data._get_axis_number(axis)
            if axis == 0:
                result = data.apply(func, axis=0, **kwargs)
            else:
                result = data.T.apply(func, axis=0, **kwargs).T  # see GH 42005

        if isinstance(result, Series):
            raise ValueError(
                f"Function {repr(func)} resulted in the apply method collapsing to a "
                f"Series.\nUsually, this is the result of the function returning a "
                f"single value, instead of list-like."
            )
        msg = (
            f"Function {repr(func)} created invalid {{0}} labels.\nUsually, this is "
            f"the result of the function returning a "
            f"{'Series' if axis is not None else 'DataFrame'} which contains invalid "
            f"labels, or returning an incorrectly shaped, list-like object which "
            f"cannot be mapped to labels, possibly due to applying the function along "
            f"the wrong axis.\n"
            f"Result {{0}} has shape: {{1}}\n"
            f"Expected {{0}} shape:   {{2}}"
        )
        if not all(result.index.isin(data.index)):
            raise ValueError(msg.format("index", result.index.shape, data.index.shape))
        if not all(result.columns.isin(data.columns)):
            raise ValueError(
                msg.format("columns", result.columns.shape, data.columns.shape)
            )
        self._update_ctx(result)
        return self
