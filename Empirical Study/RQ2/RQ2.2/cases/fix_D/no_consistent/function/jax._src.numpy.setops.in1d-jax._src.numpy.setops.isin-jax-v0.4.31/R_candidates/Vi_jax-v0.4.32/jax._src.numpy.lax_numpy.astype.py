def astype(x: ArrayLike, dtype: DTypeLike | None,
           /, *, copy: bool = False,
           device: xc.Device | Sharding | None = None) -> Array:
  """Convert an array to a specified dtype.

  JAX imlementation of :func:`numpy.astype`.

  This is implemented via :func:`jax.lax.convert_element_type`, which may
  have slightly different behavior than :func:`numpy.astype` in some cases.
  In particular, the details of float-to-int and int-to-float casts are
  implementation dependent.

  Args:
    x: input array to convert
    dtype: output dtype
    copy: if True, then always return a copy. If False (default) then only
      return a copy if necessary.
    device: optionally specify the device to which the output will be committed.

  Returns:
    An array with the same shape as ``x``, containing values of the specified
    dtype.

  See Also:
    - :func:`jax.lax.convert_element_type`: lower-level function for XLA-style
      dtype conversions.

  Examples:
    >>> x = jnp.array([0, 1, 2, 3])
    >>> x
    Array([0, 1, 2, 3], dtype=int32)
    >>> x.astype('float32')
    Array([0.0, 1.0, 2.0, 3.0], dtype=float32)

    >>> y = jnp.array([0.0, 0.5, 1.0])
    >>> y.astype(int)  # truncates fractional values
    Array([0, 0, 1], dtype=int32)
  """
  util.check_arraylike("astype", x)
  x_arr = asarray(x)

  if dtype is None:
    dtype = dtypes.canonicalize_dtype(float_)
  dtypes.check_user_dtype_supported(dtype, "astype")
  if issubdtype(x_arr.dtype, complexfloating):
    if dtypes.isdtype(dtype, ("integral", "real floating")):
      deprecations.warn(
        "jax-numpy-astype-complex-to-real",
        "Casting from complex to real dtypes will soon raise a ValueError. "
        "Please first use jnp.real or jnp.imag to take the real/imaginary "
        "component of your input.",
        stacklevel=2)
    elif np.dtype(dtype) == bool:
      # convert_element_type(complex, bool) has the wrong semantics.
      x_arr = (x_arr != _lax_const(x_arr, 0))

  # We offer a more specific warning than the usual ComplexWarning so we prefer
  # to issue our warning.
  with warnings.catch_warnings():
    warnings.simplefilter("ignore", ComplexWarning)
    result = lax_internal._convert_element_type(
      x_arr, dtype, sharding=_normalize_to_sharding(device))
  return _array_copy(result) if copy else result
