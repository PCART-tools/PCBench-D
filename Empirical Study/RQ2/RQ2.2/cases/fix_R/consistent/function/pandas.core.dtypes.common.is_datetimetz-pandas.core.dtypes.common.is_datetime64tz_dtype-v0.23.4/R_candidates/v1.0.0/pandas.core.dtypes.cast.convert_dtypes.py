def convert_dtypes(
    input_array,
    convert_string: bool = True,
    convert_integer: bool = True,
    convert_boolean: bool = True,
) -> Dtype:
    """
    Convert objects to best possible type, and optionally,
    to types supporting ``pd.NA``.

    Parameters
    ----------
    input_array : ExtensionArray or PandasArray
    convert_string : bool, default True
        Whether object dtypes should be converted to ``StringDtype()``.
    convert_integer : bool, default True
        Whether, if possible, conversion can be done to integer extension types.
    convert_boolean : bool, defaults True
        Whether object dtypes should be converted to ``BooleanDtypes()``.

    Returns
    -------
    dtype
        new dtype
    """

    if convert_string or convert_integer or convert_boolean:
        try:
            inferred_dtype = lib.infer_dtype(input_array)
        except ValueError:
            # Required to catch due to Period.  Can remove once GH 23553 is fixed
            inferred_dtype = input_array.dtype

        if not convert_string and is_string_dtype(inferred_dtype):
            inferred_dtype = input_array.dtype

        if convert_integer:
            target_int_dtype = "Int64"

            if isinstance(inferred_dtype, str) and (
                inferred_dtype == "mixed-integer"
                or inferred_dtype == "mixed-integer-float"
            ):
                inferred_dtype = target_int_dtype
            if is_integer_dtype(input_array.dtype) and not is_extension_array_dtype(
                input_array.dtype
            ):
                from pandas.core.arrays.integer import _dtypes

                inferred_dtype = _dtypes.get(input_array.dtype.name, target_int_dtype)
            if not is_integer_dtype(input_array.dtype) and is_numeric_dtype(
                input_array.dtype
            ):
                inferred_dtype = target_int_dtype

        else:
            if is_integer_dtype(inferred_dtype):
                inferred_dtype = input_array.dtype

        if convert_boolean:
            if is_bool_dtype(input_array.dtype) and not is_extension_array_dtype(
                input_array.dtype
            ):
                inferred_dtype = "boolean"
        else:
            if isinstance(inferred_dtype, str) and inferred_dtype == "boolean":
                inferred_dtype = input_array.dtype

    else:
        inferred_dtype = input_array.dtype

    return inferred_dtype
