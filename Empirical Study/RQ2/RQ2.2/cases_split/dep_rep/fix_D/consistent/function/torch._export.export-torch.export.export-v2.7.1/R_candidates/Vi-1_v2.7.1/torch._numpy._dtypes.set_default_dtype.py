def set_default_dtype(fp_dtype="numpy", int_dtype="numpy"):
    """Set the (global) defaults for fp, complex, and int dtypes.

    The complex dtype is inferred from the float (fp) dtype. It has
    a width at least twice the width of the float dtype,
    i.e., it's complex128 for float64 and complex64 for float32.

    Parameters
    ----------
    fp_dtype
        Allowed values are "numpy", "pytorch" or dtype_like things which
        can be converted into a DType instance.
        Default is "numpy" (i.e. float64).
    int_dtype
        Allowed values are "numpy", "pytorch" or dtype_like things which
        can be converted into a DType instance.
        Default is "numpy" (i.e. int64).

    Returns
    -------
    The old default dtype state: a namedtuple with attributes ``float_dtype``,
    ``complex_dtypes`` and ``int_dtype``. These attributes store *pytorch*
    dtypes.

    Notes
    ------------
    This functions has a side effect: it sets the global state with the provided dtypes.

    The complex dtype has bit width of at least twice the width of the float
    dtype, i.e. it's complex128 for float64 and complex64 for float32.

    """
    if fp_dtype not in ["numpy", "pytorch"]:
        fp_dtype = dtype(fp_dtype).torch_dtype
    if int_dtype not in ["numpy", "pytorch"]:
        int_dtype = dtype(int_dtype).torch_dtype

    if fp_dtype == "numpy":
        float_dtype = torch.float64
    elif fp_dtype == "pytorch":
        float_dtype = torch.float32
    else:
        float_dtype = fp_dtype

    complex_dtype = {
        torch.float64: torch.complex128,
        torch.float32: torch.complex64,
        torch.float16: torch.complex64,
    }[float_dtype]

    if int_dtype in ["numpy", "pytorch"]:
        int_dtype = torch.int64
    else:
        int_dtype = int_dtype

    new_defaults = _dtypes_impl.DefaultDTypes(
        float_dtype=float_dtype, complex_dtype=complex_dtype, int_dtype=int_dtype
    )

    # set the new global state and return the old state
    old_defaults = _dtypes_impl.default_dtypes
    _dtypes_impl._default_dtypes = new_defaults
    return old_defaults
