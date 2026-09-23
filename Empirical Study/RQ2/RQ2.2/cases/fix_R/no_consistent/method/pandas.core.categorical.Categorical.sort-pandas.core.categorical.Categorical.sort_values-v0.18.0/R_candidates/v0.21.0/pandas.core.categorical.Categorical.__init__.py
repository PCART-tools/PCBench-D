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
            dtype = values.dtype._from_categorical_dtype(values.dtype,
                                                         categories, ordered)
        else:
            dtype = CategoricalDtype(categories, ordered)

        # At this point, dtype is always a CategoricalDtype
        # if dtype.categories is None, we are inferring

        if fastpath:
            self._codes = coerce_indexer_dtype(values, categories)
            self._dtype = dtype
            return

        # sanitize input
        if is_categorical_dtype(values):

            # we are either a Series or a CategoricalIndex
            if isinstance(values, (ABCSeries, ABCCategoricalIndex)):
                values = values._values

            if ordered is None:
                ordered = values.ordered
            if categories is None:
                categories = values.categories
            values = values.get_values()

        elif isinstance(values, (ABCIndexClass, ABCSeries)):
            # we'll do inference later
            pass

        else:

            # on numpy < 1.6 datetimelike get inferred to all i8 by
            # _sanitize_array which is fine, but since factorize does this
            # correctly no need here this is an issue because _sanitize_array
            # also coerces np.nan to a string under certain versions of numpy
            # as well
            values = maybe_infer_to_datetimelike(values, convert_dates=True)
            if not isinstance(values, np.ndarray):
                values = _convert_to_list_like(values)
                from pandas.core.series import _sanitize_array
                # On list with NaNs, int values will be converted to float. Use
                # "object" dtype to prevent this. In the end objects will be
                # casted to int/... in the category assignment step.
                if len(values) == 0 or isna(values).any():
                    sanitize_dtype = 'object'
                else:
                    sanitize_dtype = None
                values = _sanitize_array(values, None, dtype=sanitize_dtype)

        if dtype.categories is None:
            try:
                codes, categories = factorize(values, sort=True)
            except TypeError:
                codes, categories = factorize(values, sort=False)
                if ordered:
                    # raise, as we don't have a sortable data structure and so
                    # the user should give us one by specifying categories
                    raise TypeError("'values' is not ordered, please "
                                    "explicitly specify the categories order "
                                    "by passing in a categories argument.")
            except ValueError:

                # FIXME
                raise NotImplementedError("> 1 ndim Categorical are not "
                                          "supported at this time")

            if dtype.categories is None:
                # we're inferring from values
                dtype = CategoricalDtype(categories, ordered)

        else:
            # there were two ways if categories are present
            # - the old one, where each value is a int pointer to the levels
            #   array -> not anymore possible, but code outside of pandas could
            #   call us like that, so make some checks
            # - the new one, where each value is also in the categories array
            #   (or np.nan)

            codes = _get_codes_for_values(values, dtype.categories)

            # TODO: check for old style usage. These warnings should be removes
            # after 0.18/ in 2016
            if (is_integer_dtype(values) and
                    not is_integer_dtype(dtype.categories)):
                warn("Values and categories have different dtypes. Did you "
                     "mean to use\n'Categorical.from_codes(codes, "
                     "categories)'?", RuntimeWarning, stacklevel=2)

            if (len(values) and is_integer_dtype(values) and
                    (codes == -1).all()):
                warn("None of the categories were found in values. Did you "
                     "mean to use\n'Categorical.from_codes(codes, "
                     "categories)'?", RuntimeWarning, stacklevel=2)

        self._dtype = dtype
        self._codes = coerce_indexer_dtype(codes, dtype.categories)
