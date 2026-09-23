    def __init__(self, values, categories=None, ordered=None, dtype=None,
                 fastpath=False):

        # Ways of specifying the dtype (prioritized ordered)
        # 1. dtype is a CategoricalDtype
        #    a.) with known categories, use dtype.categories
        #    b.) else with Categorical values, use values.dtype
        #    c.) else, infer from values
        #    d.) specifying dtype=CategoricalDtype and categories is an error
        # 2. dtype is a string 'category'
        #    a.) use categories, ordered
        #    b.) use values.dtype
        #    c.) infer from values
        # 3. dtype is None
        #    a.) use categories, ordered
        #    b.) use values.dtype
        #    c.) infer from values

        if dtype is not None:
            # The dtype argument takes precedence over values.dtype (if any)
            if isinstance(dtype, compat.string_types):
                if dtype == 'category':
                    dtype = CategoricalDtype(categories, ordered)
                else:
                    msg = "Unknown `dtype` {dtype}"
                    raise ValueError(msg.format(dtype=dtype))
            elif categories is not None or ordered is not None:
                raise ValueError("Cannot specify both `dtype` and `categories`"
                                 " or `ordered`.")

            categories = dtype.categories
            ordered = dtype.ordered

        elif is_categorical(values):
            # If no "dtype" was passed, use the one from "values", but honor
            # the "ordered" and "categories" arguments
            dtype = values.dtype._from_categorical_dtype(values.dtype,
                                                         categories, ordered)
        else:
            # If dtype=None and values is not categorical, create a new dtype
            dtype = CategoricalDtype(categories, ordered)

        # At this point, dtype is always a CategoricalDtype
        # if dtype.categories is None, we are inferring

        if fastpath:
            self._codes = coerce_indexer_dtype(values, categories)
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
            # _sanitize_array coerces np.nan to a string under certain versions
            # of numpy
            values = maybe_infer_to_datetimelike(values, convert_dates=True)
            if not isinstance(values, np.ndarray):
                values = _convert_to_list_like(values)
                from pandas.core.series import _sanitize_array
                # By convention, empty lists result in object dtype:
                if len(values) == 0:
                    sanitize_dtype = 'object'
                else:
                    sanitize_dtype = None
                null_mask = isna(values)
                if null_mask.any():
                    values = [values[idx] for idx in np.where(~null_mask)[0]]
                values = _sanitize_array(values, None, dtype=sanitize_dtype)

        if dtype.categories is None:
            try:
                codes, categories = factorize(values, sort=True)
            except TypeError:
                codes, categories = factorize(values, sort=False)
                if dtype.ordered:
                    # raise, as we don't have a sortable data structure and so
                    # the user should give us one by specifying categories
                    raise TypeError("'values' is not ordered, please "
                                    "explicitly specify the categories order "
                                    "by passing in a categories argument.")
            except ValueError:

                # FIXME
                raise NotImplementedError("> 1 ndim Categorical are not "
                                          "supported at this time")

            # we're inferring from values
            dtype = CategoricalDtype(categories, dtype.ordered)

        elif is_categorical_dtype(values):
            old_codes = (values.cat.codes if isinstance(values, ABCSeries)
                         else values.codes)
            codes = _recode_for_categories(old_codes, values.dtype.categories,
                                           dtype.categories)

        else:
            codes = _get_codes_for_values(values, dtype.categories)

        if null_mask.any():
            # Reinsert -1 placeholders for previously removed missing values
            full_codes = - np.ones(null_mask.shape, dtype=codes.dtype)
            full_codes[~null_mask] = codes
            codes = full_codes

        self._dtype = self._dtype.update_dtype(dtype)
        self._codes = coerce_indexer_dtype(codes, dtype.categories)
