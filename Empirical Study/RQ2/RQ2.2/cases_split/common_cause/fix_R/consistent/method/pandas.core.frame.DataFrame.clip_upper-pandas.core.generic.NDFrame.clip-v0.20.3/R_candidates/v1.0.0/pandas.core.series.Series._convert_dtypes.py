    def _convert_dtypes(
        self: ABCSeries,
        infer_objects: bool = True,
        convert_string: bool = True,
        convert_integer: bool = True,
        convert_boolean: bool = True,
    ) -> "Series":
        input_series = self
        if infer_objects:
            input_series = input_series.infer_objects()
            if is_object_dtype(input_series):
                input_series = input_series.copy()

        if convert_string or convert_integer or convert_boolean:
            inferred_dtype = convert_dtypes(
                input_series._values, convert_string, convert_integer, convert_boolean
            )
            try:
                result = input_series.astype(inferred_dtype)
            except TypeError:
                result = input_series.copy()
        else:
            result = input_series.copy()
        return result
