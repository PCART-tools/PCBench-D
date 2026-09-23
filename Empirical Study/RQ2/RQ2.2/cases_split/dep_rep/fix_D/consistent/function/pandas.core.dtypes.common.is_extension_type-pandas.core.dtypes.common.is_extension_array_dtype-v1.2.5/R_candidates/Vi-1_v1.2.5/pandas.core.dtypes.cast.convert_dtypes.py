def convert_dtypes(
    input_array: AnyArrayLike,
    convert_string: bool = True,
    convert_integer: bool = True,
    convert_boolean: bool = True,
    convert_floating: bool = True,
) -> Dtype:
    """
    Convert objects to best possible type, and optionally,
    to types supporting ``pd.NA``.

    Parameters
    ----------
    input_array : ExtensionArray, Index, Series or np.ndarray
    convert_string : bool, default True
        Whether object dtypes should be converted to ``StringDtype()``.
    convert_integer : bool, default True
        Whether, if possible, conversion can be done to integer extension types.
    convert_boolean : bool, defaults True
        Whether object dtypes should be converted to ``BooleanDtypes()``.
    convert_floating : bool, defaults True
        Whether, if possible, conversion can be done to floating extension types.
        If `convert_integer` is also True, preference will be give to integer
        dtypes if the floats can be faithfully casted to integers.

    Returns
    -------
    dtype
        new dtype
    """
    is_extension = is_extension_array_dtype(input_array.dtype)
    if (
        convert_string or convert_integer or convert_boolean or convert_floating
    ) and not is_extension:
        try:
            inferred_dtype = lib.infer_dtype(input_array)
        except ValueError:
            # Required to catch due to Period.  Can remove once GH 23553 is fixed
            inferred_dtype = input_array.dtype

        if not convert_string and is_string_dtype(inferred_dtype):
            inferred_dtype = input_array.dtype

        if convert_integer:
            target_int_dtype = "Int64"

            if is_integer_dtype(input_array.dtype):
                from pandas.core.arrays.integer import INT_STR_TO_DTYPE

                inferred_dtype = INT_STR_TO_DTYPE.get(
                    input_array.dtype.name, target_int_dtype
                )
            if not is_integer_dtype(input_array.dtype) and is_numeric_dtype(
                input_array.dtype
            ):
                inferred_dtype = target_int_dtype

        else:
            if is_integer_dtype(inferred_dtype):
                inferred_dtype = input_array.dtype

        if convert_floating:
            if not is_integer_dtype(input_array.dtype) and is_numeric_dtype(
                input_array.dtype
            ):
                from pandas.core.arrays.floating import FLOAT_STR_TO_DTYPE

                inferred_float_dtype = FLOAT_STR_TO_DTYPE.get(
                    input_array.dtype.name, "Float64"
                )
                # if we could also convert to integer, check if all floats
                # are actually integers
                if convert_integer:
                    arr = input_array[notna(input_array)]
                    if (arr.astype(int) == arr).all():
                        inferred_dtype = "Int64"
                    else:
                        inferred_dtype = inferred_float_dtype
                else:
                    inferred_dtype = inferred_float_dtype
        else:
            if is_float_dtype(inferred_dtype):
                inferred_dtype = input_array.dtype

        if convert_boolean:
            if is_bool_dtype(input_array.dtype):
                inferred_dtype = "boolean"
        else:
            if isinstance(inferred_dtype, str) and inferred_dtype == "boolean":
                inferred_dtype = input_array.dtype

    else:
        inferred_dtype = input_array.dtype

    return inferred_dtype
