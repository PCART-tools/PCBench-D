    @staticmethod
    def _validate(data):
        """
        Auxiliary function for StringMethods, infers and checks dtype of data.

        This is a "first line of defence" at the creation of the StringMethods-
        object (see _make_accessor), and just checks that the dtype is in the
        *union* of the allowed types over all string methods below; this
        restriction is then refined on a per-method basis using the decorator
        @forbid_nonstring_types (more info in the corresponding docstring).

        This really should exclude all series/index with any non-string values,
        but that isn't practical for performance reasons until we have a str
        dtype (GH 9343 / 13877)

        Parameters
        ----------
        data : The content of the Series

        Returns
        -------
        dtype : inferred dtype of data
        """
        from pandas import StringDtype

        if isinstance(data, ABCMultiIndex):
            raise AttributeError(
                "Can only use .str accessor with Index, not MultiIndex"
            )

        # see _libs/lib.pyx for list of inferred types
        allowed_types = ["string", "empty", "bytes", "mixed", "mixed-integer"]

        values = getattr(data, "values", data)  # Series / Index
        values = getattr(values, "categories", values)  # categorical / normal

        # explicitly allow StringDtype
        if isinstance(values.dtype, StringDtype):
            return "string"

        try:
            inferred_dtype = lib.infer_dtype(values, skipna=True)
        except ValueError:
            # GH#27571 mostly occurs with ExtensionArray
            inferred_dtype = None

        if inferred_dtype not in allowed_types:
            raise AttributeError("Can only use .str accessor with string values!")
        return inferred_dtype
