def convert_dtypes(
    input_array: ArrayLike,
    convert_string: bool = True,
    convert_integer: bool = True,
    convert_boolean: bool = True,
    convert_floating: bool = True,
    infer_objects: bool = False,
    dtype_backend: Literal["numpy_nullable", "pyarrow"] = "numpy_nullable",
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
    infer_objects : bool, defaults False
        Whether to also infer objects to float/int if possible. Is only hit if the
        object array contains pd.NA.
    dtype_backend : {'numpy_nullable', 'pyarrow'}, default 'numpy_nullable'
        Back-end data type applied to the resultant :class:`DataFrame`
        (still experimental). Behaviour is as follows:

        * ``"numpy_nullable"``: returns nullable-dtype-backed :class:`DataFrame`
          (default).
        * ``"pyarrow"``: returns pyarrow-backed nullable :class:`ArrowDtype`
          DataFrame.

        .. versionadded:: 2.0

    Returns
    -------
    np.dtype, or ExtensionDtype
    """
    inferred_dtype: str | DtypeObj

    if (
        convert_string or convert_integer or convert_boolean or convert_floating
    ) and isinstance(input_array, np.ndarray):
        if input_array.dtype == object:
            inferred_dtype = lib.infer_dtype(input_array)
        else:
            inferred_dtype = input_array.dtype

        if is_string_dtype(inferred_dtype):
            if not convert_string or inferred_dtype == "bytes":
                inferred_dtype = input_array.dtype
            else:
                inferred_dtype = pandas_dtype_func("string")

        if convert_integer:
            target_int_dtype = pandas_dtype_func("Int64")

            if input_array.dtype.kind in "iu":
                from pandas.core.arrays.integer import NUMPY_INT_TO_DTYPE

                inferred_dtype = NUMPY_INT_TO_DTYPE.get(
                    input_array.dtype, target_int_dtype
                )
            elif input_array.dtype.kind in "fcb":
                # TODO: de-dup with maybe_cast_to_integer_array?
                arr = input_array[notna(input_array)]
                if (arr.astype(int) == arr).all():
                    inferred_dtype = target_int_dtype
                else:
                    inferred_dtype = input_array.dtype
            elif (
                infer_objects
                and input_array.dtype == object
                and (isinstance(inferred_dtype, str) and inferred_dtype == "integer")
            ):
                inferred_dtype = target_int_dtype

        if convert_floating:
            if input_array.dtype.kind in "fcb":
                # i.e. numeric but not integer
                from pandas.core.arrays.floating import NUMPY_FLOAT_TO_DTYPE

                inferred_float_dtype: DtypeObj = NUMPY_FLOAT_TO_DTYPE.get(
                    input_array.dtype, pandas_dtype_func("Float64")
                )
                # if we could also convert to integer, check if all floats
                # are actually integers
                if convert_integer:
                    # TODO: de-dup with maybe_cast_to_integer_array?
                    arr = input_array[notna(input_array)]
                    if (arr.astype(int) == arr).all():
                        inferred_dtype = pandas_dtype_func("Int64")
                    else:
                        inferred_dtype = inferred_float_dtype
                else:
                    inferred_dtype = inferred_float_dtype
            elif (
                infer_objects
                and input_array.dtype == object
                and (
                    isinstance(inferred_dtype, str)
                    and inferred_dtype == "mixed-integer-float"
                )
            ):
                inferred_dtype = pandas_dtype_func("Float64")

        if convert_boolean:
            if input_array.dtype.kind == "b":
                inferred_dtype = pandas_dtype_func("boolean")
            elif isinstance(inferred_dtype, str) and inferred_dtype == "boolean":
                inferred_dtype = pandas_dtype_func("boolean")

        if isinstance(inferred_dtype, str):
            # If we couldn't do anything else, then we retain the dtype
            inferred_dtype = input_array.dtype

    else:
        inferred_dtype = input_array.dtype

    if dtype_backend == "pyarrow":
        from pandas.core.arrays.arrow.array import to_pyarrow_type
        from pandas.core.arrays.string_ import StringDtype

        assert not isinstance(inferred_dtype, str)

        if (
            (convert_integer and inferred_dtype.kind in "iu")
            or (convert_floating and inferred_dtype.kind in "fc")
            or (convert_boolean and inferred_dtype.kind == "b")
            or (convert_string and isinstance(inferred_dtype, StringDtype))
            or (
                inferred_dtype.kind not in "iufcb"
                and not isinstance(inferred_dtype, StringDtype)
            )
        ):
            if isinstance(inferred_dtype, PandasExtensionDtype) and not isinstance(
                inferred_dtype, DatetimeTZDtype
            ):
                base_dtype = inferred_dtype.base
            elif isinstance(inferred_dtype, (BaseMaskedDtype, ArrowDtype)):
                base_dtype = inferred_dtype.numpy_dtype
            elif isinstance(inferred_dtype, StringDtype):
                base_dtype = np.dtype(str)
            else:
                base_dtype = inferred_dtype
            pa_type = to_pyarrow_type(base_dtype)
            if pa_type is not None:
                inferred_dtype = ArrowDtype(pa_type)
    elif dtype_backend == "numpy_nullable" and isinstance(inferred_dtype, ArrowDtype):
        # GH 53648
        inferred_dtype = _arrow_dtype_mapping()[inferred_dtype.pyarrow_dtype]

    # error: Incompatible return value type (got "Union[str, Union[dtype[Any],
    # ExtensionDtype]]", expected "Union[dtype[Any], ExtensionDtype]")
    return inferred_dtype  # type: ignore[return-value]
