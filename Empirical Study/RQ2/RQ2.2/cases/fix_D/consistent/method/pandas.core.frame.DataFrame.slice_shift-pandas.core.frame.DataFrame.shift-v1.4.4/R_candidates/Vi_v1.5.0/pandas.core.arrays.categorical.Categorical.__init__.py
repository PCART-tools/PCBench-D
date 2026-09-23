    def __init__(
        self,
        values,
        categories=None,
        ordered=None,
        dtype: Dtype | None = None,
        fastpath: bool = False,
        copy: bool = True,
    ) -> None:

        dtype = CategoricalDtype._from_values_or_dtype(
            values, categories, ordered, dtype
        )
        # At this point, dtype is always a CategoricalDtype, but
        # we may have dtype.categories be None, and we need to
        # infer categories in a factorization step further below

        if fastpath:
            codes = coerce_indexer_dtype(values, dtype.categories)
            dtype = CategoricalDtype(ordered=False).update_dtype(dtype)
            super().__init__(codes, dtype)
            return

        if not is_list_like(values):
            # GH#38433
            warn(
                "Allowing scalars in the Categorical constructor is deprecated "
                "and will raise in a future version.  Use `[value]` instead",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
            values = [values]

        # null_mask indicates missing values we want to exclude from inference.
        # This means: only missing values in list-likes (not arrays/ndframes).
        null_mask = np.array(False)

        # sanitize input
        if is_categorical_dtype(values):
            if dtype.categories is None:
                dtype = CategoricalDtype(values.categories, dtype.ordered)
        elif not isinstance(values, (ABCIndex, ABCSeries, ExtensionArray)):
            values = com.convert_to_list_like(values)
            if isinstance(values, list) and len(values) == 0:
                # By convention, empty lists result in object dtype:
                values = np.array([], dtype=object)
            elif isinstance(values, np.ndarray):
                if values.ndim > 1:
                    # preempt sanitize_array from raising ValueError
                    raise NotImplementedError(
                        "> 1 ndim Categorical are not supported at this time"
                    )
                values = sanitize_array(values, None)
            else:
                # i.e. must be a list
                arr = sanitize_array(values, None)
                null_mask = isna(arr)
                if null_mask.any():
                    # We remove null values here, then below will re-insert
                    #  them, grep "full_codes"
                    arr_list = [values[idx] for idx in np.where(~null_mask)[0]]

                    # GH#44900 Do not cast to float if we have only missing values
                    if arr_list or arr.dtype == "object":
                        sanitize_dtype = None
                    else:
                        sanitize_dtype = arr.dtype

                    arr = sanitize_array(arr_list, None, dtype=sanitize_dtype)
                values = arr

        if dtype.categories is None:
            try:
                codes, categories = factorize(values, sort=True)
            except TypeError as err:
                codes, categories = factorize(values, sort=False)
                if dtype.ordered:
                    # raise, as we don't have a sortable data structure and so
                    # the user should give us one by specifying categories
                    raise TypeError(
                        "'values' is not ordered, please "
                        "explicitly specify the categories order "
                        "by passing in a categories argument."
                    ) from err

            # we're inferring from values
            dtype = CategoricalDtype(categories, dtype.ordered)

        elif is_categorical_dtype(values.dtype):
            old_codes = extract_array(values)._codes
            codes = recode_for_categories(
                old_codes, values.dtype.categories, dtype.categories, copy=copy
            )

        else:
            codes = _get_codes_for_values(values, dtype.categories)

        if null_mask.any():
            # Reinsert -1 placeholders for previously removed missing values
            full_codes = -np.ones(null_mask.shape, dtype=codes.dtype)
            full_codes[~null_mask] = codes
            codes = full_codes

        dtype = CategoricalDtype(ordered=False).update_dtype(dtype)
        arr = coerce_indexer_dtype(codes, dtype.categories)
        super().__init__(arr, dtype)
