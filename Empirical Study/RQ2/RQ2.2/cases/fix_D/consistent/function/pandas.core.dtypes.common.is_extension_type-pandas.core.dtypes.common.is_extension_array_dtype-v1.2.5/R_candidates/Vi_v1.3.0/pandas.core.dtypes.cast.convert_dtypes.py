def convert_dtypes(
    input_array: ArrayLike,
    convert_string: bool = True,
    convert_integer: bool = True,
    convert_boolean: bool = True,
    convert_floating: bool = True,
) -> DtypeObj:
    """
    Convert objects to best possible type, and optionally,
    to types supporting ``pd.NA``.

    Parameters
    ----------
    input_array : ExtensionArray or np.ndarray
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
    np.dtype, or ExtensionDtype
    """
    inferred_dtype: str | DtypeObj

    if (
        convert_string or convert_integer or convert_boolean or convert_floating
    ) and isinstance(input_array, np.ndarray):

        if is_object_dtype(input_array.dtype):
            inferred_dtype = lib.infer_dtype(input_array)
        else:
            inferred_dtype = input_array.dtype

        if is_string_dtype(inferred_dtype):
            if not convert_string:
                return input_array.dtype
            else:
                return pandas_dtype("string")

        if convert_integer:
            target_int_dtype = pandas_dtype("Int64")

            if is_integer_dtype(input_array.dtype):
                from pandas.core.arrays.integer import INT_STR_TO_DTYPE

                inferred_dtype = INT_STR_TO_DTYPE.get(
                    input_array.dtype.name, target_int_dtype
                )
            elif is_numeric_dtype(input_array.dtype):
                # TODO: de-dup with maybe_cast_to_integer_array?
                arr = input_array[notna(input_array)]
                if (arr.astype(int) == arr).all():
                    inferred_dtype = target_int_dtype
                else:
                    inferred_dtype = input_array.dtype

        if convert_floating:
            if not is_integer_dtype(input_array.dtype) and is_numeric_dtype(
                input_array.dtype
            ):
                from pandas.core.arrays.floating import FLOAT_STR_TO_DTYPE

                inferred_float_dtype: DtypeObj = FLOAT_STR_TO_DTYPE.get(
                    input_array.dtype.name, pandas_dtype("Float64")
                )
                # if we could also convert to integer, check if all floats
                # are actually integers
                if convert_integer:
                    # TODO: de-dup with maybe_cast_to_integer_array?
                    arr = input_array[notna(input_array)]
                    if (arr.astype(int) == arr).all():
                        inferred_dtype = pandas_dtype("Int64")
                    else:
                        inferred_dtype = inferred_float_dtype
                else:
                    inferred_dtype = inferred_float_dtype

        if convert_boolean:
            if is_bool_dtype(input_array.dtype):
                inferred_dtype = pandas_dtype("boolean")
            elif isinstance(inferred_dtype, str) and inferred_dtype == "boolean":
                inferred_dtype = pandas_dtype("boolean")

        if isinstance(inferred_dtype, str):
            # If we couldn't do anything else, then we retain the dtype
            inferred_dtype = input_array.dtype

    else:
        return input_array.dtype

    # error: Incompatible return value type (got "Union[str, Union[dtype[Any],
    # ExtensionDtype]]", expected "Union[dtype[Any], ExtensionDtype]")
    return inferred_dtype  # type: ignore[return-value]
