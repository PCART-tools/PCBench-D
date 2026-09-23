    @staticmethod
    def _validate(data):
        from pandas.core.index import Index

        if (isinstance(data, ABCSeries) and
                not ((is_categorical_dtype(data.dtype) and
                      is_object_dtype(data.values.categories)) or
                     (is_object_dtype(data.dtype)))):
            # it's neither a string series not a categorical series with
            # strings inside the categories.
            # this really should exclude all series with any non-string values
            # (instead of test for object dtype), but that isn't practical for
            # performance reasons until we have a str dtype (GH 9343)
            raise AttributeError("Can only use .str accessor with string "
                                 "values, which use np.object_ dtype in "
                                 "pandas")
        elif isinstance(data, Index):
            # can't use ABCIndex to exclude non-str

            # see src/inference.pyx which can contain string values
            allowed_types = ('string', 'unicode', 'mixed', 'mixed-integer')
            if is_categorical_dtype(data.dtype):
                inf_type = data.categories.inferred_type
            else:
                inf_type = data.inferred_type
            if inf_type not in allowed_types:
                message = ("Can only use .str accessor with string values "
                           "(i.e. inferred_type is 'string', 'unicode' or "
                           "'mixed')")
                raise AttributeError(message)
            if data.nlevels > 1:
                message = ("Can only use .str accessor with Index, not "
                           "MultiIndex")
                raise AttributeError(message)
