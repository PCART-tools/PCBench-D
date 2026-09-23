    def __init__(
        self, values, categories=None, ordered=None, dtype=None, fastpath=False
    ):

        dtype = CategoricalDtype._from_values_or_dtype(
            values, categories, ordered, dtype
        )
        # At this point, dtype is always a CategoricalDtype, but
        # we may have dtype.categories be None, and we need to
        # infer categories in a factorization step further below

        if fastpath:
            self._codes = coerce_indexer_dtype(values, dtype.categories)
            self._dtype = self._dtype.update_dtype(dtype)
            return

        # null_mask indicates missing values we want to exclude from inference.
        # This means: only missing values in list-likes (not arrays/ndframes).
        null_mask = np.array(False)

        # sanitize input
        if is_categorical_dtype(values):
            if dtype.categories is None:
                dtype = CategoricalDtype(values.categories, dtype.ordered)
        elif not isinstance(values, (ABCIndexClass, ABCSeries)):
            # sanitize_array coerces np.nan to a string under certain versions
            # of numpy
            values = maybe_infer_to_datetimelike(values, convert_dates=True)
            if not isinstance(values, np.ndarray):
                values = com.convert_to_list_like(values)

                # By convention, empty lists result in object dtype:
                sanitize_dtype = np.dtype("O") if len(values) == 0 else None
                null_mask = isna(values)
                if null_mask.any():
                    values = [values[idx] for idx in np.where(~null_mask)[0]]
                values = sanitize_array(values, None, dtype=sanitize_dtype)

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
            except ValueError as err:

                # TODO(EA2D)
                raise NotImplementedError(
                    "> 1 ndim Categorical are not supported at this time"
                ) from err

            # we're inferring from values
            dtype = CategoricalDtype(categories, dtype.ordered)

        elif is_categorical_dtype(values.dtype):
            old_codes = (
                values._values.codes if isinstance(values, ABCSeries) else values.codes
            )
            codes = recode_for_categories(
                old_codes, values.dtype.categories, dtype.categories
            )

        else:
            codes = _get_codes_for_values(values, dtype.categories)

        if null_mask.any():
            # Reinsert -1 placeholders for previously removed missing values
            full_codes = -np.ones(null_mask.shape, dtype=codes.dtype)
            full_codes[~null_mask] = codes
            codes = full_codes

        self._dtype = self._dtype.update_dtype(dtype)
        self._codes = coerce_indexer_dtype(codes, dtype.categories)
