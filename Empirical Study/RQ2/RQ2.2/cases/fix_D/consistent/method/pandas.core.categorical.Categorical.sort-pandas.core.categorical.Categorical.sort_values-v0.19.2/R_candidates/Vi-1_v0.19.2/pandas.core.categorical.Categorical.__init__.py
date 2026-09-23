    def __init__(self, values, categories=None, ordered=False,
                 name=None, fastpath=False):

        self._validate_ordered(ordered)

        if fastpath:
            # fast path
            self._codes = _coerce_indexer_dtype(values, categories)
            self._categories = self._validate_categories(
                categories, fastpath=isinstance(categories, ABCIndexClass))
            self._ordered = ordered
            return

        if name is not None:
            msg = ("the 'name' keyword is removed, use 'name' with consumers "
                   "of the categorical instead (e.g. 'Series(cat, "
                   "name=\"something\")'")
            warn(msg, UserWarning, stacklevel=2)

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
            pass

        else:

            # on numpy < 1.6 datetimelike get inferred to all i8 by
            # _sanitize_array which is fine, but since factorize does this
            # correctly no need here this is an issue because _sanitize_array
            # also coerces np.nan to a string under certain versions of numpy
            # as well
            values = _possibly_infer_to_datetimelike(values,
                                                     convert_dates=True)
            if not isinstance(values, np.ndarray):
                values = _convert_to_list_like(values)
                from pandas.core.series import _sanitize_array
                # On list with NaNs, int values will be converted to float. Use
                # "object" dtype to prevent this. In the end objects will be
                # casted to int/... in the category assignment step.
                dtype = 'object' if isnull(values).any() else None
                values = _sanitize_array(values, None, dtype=dtype)

        if categories is None:
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

            categories = self._validate_categories(categories)

        else:
            # there were two ways if categories are present
            # - the old one, where each value is a int pointer to the levels
            #   array -> not anymore possible, but code outside of pandas could
            #   call us like that, so make some checks
            # - the new one, where each value is also in the categories array
            #   (or np.nan)

            # make sure that we always have the same type here, no matter what
            # we get passed in
            categories = self._validate_categories(categories)
            codes = _get_codes_for_values(values, categories)

            # TODO: check for old style usage. These warnings should be removes
            # after 0.18/ in 2016
            if is_integer_dtype(values) and not is_integer_dtype(categories):
                warn("Values and categories have different dtypes. Did you "
                     "mean to use\n'Categorical.from_codes(codes, "
                     "categories)'?", RuntimeWarning, stacklevel=2)

            if (len(values) and is_integer_dtype(values) and
                    (codes == -1).all()):
                warn("None of the categories were found in values. Did you "
                     "mean to use\n'Categorical.from_codes(codes, "
                     "categories)'?", RuntimeWarning, stacklevel=2)

        self.set_ordered(ordered or False, inplace=True)
        self._categories = categories
        self._codes = _coerce_indexer_dtype(codes, categories)
