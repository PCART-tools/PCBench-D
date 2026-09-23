    @final
    def _get_cythonized_result(
        self,
        base_func: Callable,
        cython_dtype: np.dtype,
        numeric_only: bool | lib.NoDefault = lib.no_default,
        needs_counts: bool = False,
        needs_nullable: bool = False,
        needs_mask: bool = False,
        pre_processing=None,
        post_processing=None,
        **kwargs,
    ):
        """
        Get result for Cythonized functions.

        Parameters
        ----------
        base_func : callable, Cythonized function to be called
        cython_dtype : np.dtype
            Type of the array that will be modified by the Cython call.
        numeric_only : bool, default True
            Whether only numeric datatypes should be computed
        needs_counts : bool, default False
            Whether the counts should be a part of the Cython call
        needs_mask : bool, default False
            Whether boolean mask needs to be part of the Cython call
            signature
        needs_nullable : bool, default False
            Whether a bool specifying if the input is nullable is part
            of the Cython call signature
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
        **kwargs : dict
            Extra arguments to be passed back to Cython funcs

        Returns
        -------
        `Series` or `DataFrame`  with filled values
        """
        numeric_only = self._resolve_numeric_only(numeric_only)

        if post_processing and not callable(post_processing):
            raise ValueError("'post_processing' must be a callable!")
        if pre_processing and not callable(pre_processing):
            raise ValueError("'pre_processing' must be a callable!")

        grouper = self.grouper

        ids, _, ngroups = grouper.group_info

        how = base_func.__name__
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
                counts = np.zeros(self.ngroups, dtype=np.int64)
                func = partial(func, counts=counts)

            vals = values
            if pre_processing:
                vals, inferences = pre_processing(vals)

            vals = vals.astype(cython_dtype, copy=False)
            if vals.ndim == 1:
                vals = vals.reshape((-1, 1))
            func = partial(func, values=vals)

            if needs_mask:
                mask = isna(values).view(np.uint8)
                if mask.ndim == 1:
                    mask = mask.reshape(-1, 1)
                func = partial(func, mask=mask)

            if needs_nullable:
                is_nullable = isinstance(values, BaseMaskedArray)
                func = partial(func, nullable=is_nullable)

            func(**kwargs)  # Call func to modify indexer values in place

            if values.ndim == 1:
                assert result.shape[1] == 1, result.shape
                result = result[:, 0]

            if post_processing:
                pp_kwargs = {}
                if needs_nullable:
                    pp_kwargs["nullable"] = isinstance(values, BaseMaskedArray)

                result = post_processing(result, inferences, **pp_kwargs)

            return result.T

        obj = self._obj_with_exclusions

        # Operate block-wise instead of column-by-column
        is_ser = obj.ndim == 1
        mgr = self._get_data_to_aggregate()

        if numeric_only:
            mgr = mgr.get_numeric_data()

        res_mgr = mgr.grouped_reduce(blk_func, ignore_failures=True)

        if not is_ser and len(res_mgr.items) != len(mgr.items):
            howstr = how.replace("group_", "")
            warn_dropping_nuisance_columns_deprecated(type(self), howstr)

            if len(res_mgr.items) == 0:
                # We re-call grouped_reduce to get the right exception message
                mgr.grouped_reduce(blk_func, ignore_failures=False)
                # grouped_reduce _should_ raise, so this should not be reached
                raise TypeError(  # pragma: no cover
                    "All columns were dropped in grouped_reduce"
                )

        if is_ser:
            out = self._wrap_agged_manager(res_mgr)
        else:
            out = obj._constructor(res_mgr)

        return self._wrap_aggregated_output(out)
