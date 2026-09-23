    @final
    def _get_cythonized_result(
        self,
        base_func: Callable,
        cython_dtype: np.dtype,
        numeric_only: bool = False,
        needs_counts: bool = False,
        pre_processing=None,
        post_processing=None,
        how: str = "any_all",
        **kwargs,
    ):
        """
        Get result for Cythonized functions.

        Parameters
        ----------
        base_func : callable, Cythonized function to be called
        cython_dtype : np.dtype
            Type of the array that will be modified by the Cython call.
        numeric_only : bool, default False
            Whether only numeric datatypes should be computed
        needs_counts : bool, default False
            Whether the counts should be a part of the Cython call
        pre_processing : function, default None
            Function to be applied to `values` prior to passing to Cython.
            Function should return a tuple where the first element is the
            values to be passed to Cython and the second element is an optional
            type which the values should be converted to after being returned
            by the Cython operation. This function is also responsible for
            raising a TypeError if the values have an invalid type. Raises
            if `needs_values` is False.
        post_processing : function, default None
            Function to be applied to result of Cython function. Should accept
            an array of values as the first argument and type inferences as its
            second argument, i.e. the signature should be
            (ndarray, Type). If `needs_nullable=True`, a third argument should be
            `nullable`, to allow for processing specific to nullable values.
        how : str, default any_all
            Determines if any/all cython interface or std interface is used.
        **kwargs : dict
            Extra arguments to be passed back to Cython funcs

        Returns
        -------
        `Series` or `DataFrame`  with filled values
        """
        if post_processing and not callable(post_processing):
            raise ValueError("'post_processing' must be a callable!")
        if pre_processing and not callable(pre_processing):
            raise ValueError("'pre_processing' must be a callable!")

        grouper = self.grouper

        ids, _, ngroups = grouper.group_info

        base_func = partial(base_func, labels=ids)

        def blk_func(values: ArrayLike) -> ArrayLike:
            values = values.T
            ncols = 1 if values.ndim == 1 else values.shape[1]

            result: ArrayLike
            result = np.zeros(ngroups * ncols, dtype=cython_dtype)
            result = result.reshape((ngroups, ncols))

            func = partial(base_func, out=result)

            inferences = None

            if needs_counts:
                counts = np.zeros(ngroups, dtype=np.int64)
                func = partial(func, counts=counts)

            is_datetimelike = values.dtype.kind in ["m", "M"]
            vals = values
            if is_datetimelike and how == "std":
                vals = vals.view("i8")
            if pre_processing:
                vals, inferences = pre_processing(vals)

            vals = vals.astype(cython_dtype, copy=False)
            if vals.ndim == 1:
                vals = vals.reshape((-1, 1))
            func = partial(func, values=vals)

            if how != "std" or isinstance(values, BaseMaskedArray):
                mask = isna(values).view(np.uint8)
                if mask.ndim == 1:
                    mask = mask.reshape(-1, 1)
                func = partial(func, mask=mask)

            if how != "std":
                is_nullable = isinstance(values, BaseMaskedArray)
                func = partial(func, nullable=is_nullable)

            elif isinstance(values, BaseMaskedArray):
                result_mask = np.zeros(result.shape, dtype=np.bool_)
                func = partial(func, result_mask=result_mask)

            # Call func to modify result in place
            if how == "std":
                func(**kwargs, is_datetimelike=is_datetimelike)
            else:
                func(**kwargs)

            if values.ndim == 1:
                assert result.shape[1] == 1, result.shape
                result = result[:, 0]

            if post_processing:
                pp_kwargs: dict[str, bool | np.ndarray] = {}
                pp_kwargs["nullable"] = isinstance(values, BaseMaskedArray)
                if how == "std" and pp_kwargs["nullable"]:
                    pp_kwargs["result_mask"] = result_mask

                result = post_processing(result, inferences, **pp_kwargs)

            if how == "std" and is_datetimelike:
                values = cast("DatetimeArray | TimedeltaArray", values)
                unit = values.unit
                with warnings.catch_warnings():
                    # suppress "RuntimeWarning: invalid value encountered in cast"
                    warnings.filterwarnings("ignore")
                    result = result.astype(np.int64, copy=False)
                result = result.view(f"m8[{unit}]")

            return result.T

        # Operate block-wise instead of column-by-column
        mgr = self._get_data_to_aggregate(numeric_only=numeric_only, name=how)

        res_mgr = mgr.grouped_reduce(blk_func)

        out = self._wrap_agged_manager(res_mgr)
        return self._wrap_aggregated_output(out)
