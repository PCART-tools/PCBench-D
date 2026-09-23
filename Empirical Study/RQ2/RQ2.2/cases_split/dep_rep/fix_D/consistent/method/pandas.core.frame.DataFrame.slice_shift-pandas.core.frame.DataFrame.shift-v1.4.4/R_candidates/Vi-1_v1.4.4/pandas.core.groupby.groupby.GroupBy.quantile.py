    @final
    def quantile(self, q=0.5, interpolation: str = "linear"):
        """
        Return group values at the given quantile, a la numpy.percentile.

        Parameters
        ----------
        q : float or array-like, default 0.5 (50% quantile)
            Value(s) between 0 and 1 providing the quantile(s) to compute.
        interpolation : {'linear', 'lower', 'higher', 'midpoint', 'nearest'}
            Method to use when the desired quantile falls between two points.

        Returns
        -------
        Series or DataFrame
            Return type determined by caller of GroupBy object.

        See Also
        --------
        Series.quantile : Similar method for Series.
        DataFrame.quantile : Similar method for DataFrame.
        numpy.percentile : NumPy method to compute qth percentile.

        Examples
        --------
        >>> df = pd.DataFrame([
        ...     ['a', 1], ['a', 2], ['a', 3],
        ...     ['b', 1], ['b', 3], ['b', 5]
        ... ], columns=['key', 'val'])
        >>> df.groupby('key').quantile()
            val
        key
        a    2.0
        b    3.0
        """

        def pre_processor(vals: ArrayLike) -> tuple[np.ndarray, np.dtype | None]:
            if is_object_dtype(vals):
                raise TypeError(
                    "'quantile' cannot be performed against 'object' dtypes!"
                )

            inference: np.dtype | None = None
            if is_integer_dtype(vals.dtype):
                if isinstance(vals, ExtensionArray):
                    out = vals.to_numpy(dtype=float, na_value=np.nan)
                else:
                    out = vals
                inference = np.dtype(np.int64)
            elif is_bool_dtype(vals.dtype) and isinstance(vals, ExtensionArray):
                out = vals.to_numpy(dtype=float, na_value=np.nan)
            elif is_datetime64_dtype(vals.dtype):
                inference = np.dtype("datetime64[ns]")
                out = np.asarray(vals).astype(float)
            elif is_timedelta64_dtype(vals.dtype):
                inference = np.dtype("timedelta64[ns]")
                out = np.asarray(vals).astype(float)
            elif isinstance(vals, ExtensionArray) and is_float_dtype(vals):
                inference = np.dtype(np.float64)
                out = vals.to_numpy(dtype=float, na_value=np.nan)
            else:
                out = np.asarray(vals)

            return out, inference

        def post_processor(vals: np.ndarray, inference: np.dtype | None) -> np.ndarray:
            if inference:
                # Check for edge case
                if not (
                    is_integer_dtype(inference)
                    and interpolation in {"linear", "midpoint"}
                ):
                    vals = vals.astype(inference)

            return vals

        orig_scalar = is_scalar(q)
        if orig_scalar:
            q = [q]

        qs = np.array(q, dtype=np.float64)
        ids, _, ngroups = self.grouper.group_info
        nqs = len(qs)

        func = partial(
            libgroupby.group_quantile, labels=ids, qs=qs, interpolation=interpolation
        )

        # Put '-1' (NaN) labels as the last group so it does not interfere
        # with the calculations. Note: length check avoids failure on empty
        # labels. In that case, the value doesn't matter
        na_label_for_sorting = ids.max() + 1 if len(ids) > 0 else 0
        labels_for_lexsort = np.where(ids == -1, na_label_for_sorting, ids)

        def blk_func(values: ArrayLike) -> ArrayLike:
            mask = isna(values)
            vals, inference = pre_processor(values)

            ncols = 1
            if vals.ndim == 2:
                ncols = vals.shape[0]
                shaped_labels = np.broadcast_to(
                    labels_for_lexsort, (ncols, len(labels_for_lexsort))
                )
            else:
                shaped_labels = labels_for_lexsort

            out = np.empty((ncols, ngroups, nqs), dtype=np.float64)

            # Get an index of values sorted by values and then labels
            order = (vals, shaped_labels)
            sort_arr = np.lexsort(order).astype(np.intp, copy=False)

            if vals.ndim == 1:
                func(out[0], values=vals, mask=mask, sort_indexer=sort_arr)
            else:
                for i in range(ncols):
                    func(out[i], values=vals[i], mask=mask[i], sort_indexer=sort_arr[i])

            if vals.ndim == 1:
                out = out.ravel("K")
            else:
                out = out.reshape(ncols, ngroups * nqs)
            return post_processor(out, inference)

        obj = self._obj_with_exclusions
        is_ser = obj.ndim == 1
        mgr = self._get_data_to_aggregate()

        res_mgr = mgr.grouped_reduce(blk_func, ignore_failures=True)
        if not is_ser and len(res_mgr.items) != len(mgr.items):
            warn_dropping_nuisance_columns_deprecated(type(self), "quantile")

            if len(res_mgr.items) == 0:
                # re-call grouped_reduce to get the desired exception message
                mgr.grouped_reduce(blk_func, ignore_failures=False)
                # grouped_reduce _should_ raise, so this should not be reached
                raise TypeError(  # pragma: no cover
                    "All columns were dropped in grouped_reduce"
                )

        if is_ser:
            res = self._wrap_agged_manager(res_mgr)
        else:
            res = obj._constructor(res_mgr)

        if orig_scalar:
            # Avoid expensive MultiIndex construction
            return self._wrap_aggregated_output(res)
        return self._wrap_aggregated_output(res, qs=qs)
