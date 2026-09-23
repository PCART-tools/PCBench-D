@util._wraps(np.array, lax_description=_ARRAY_DOC)
def array(object: Any, dtype: DTypeLike | None = None, copy: bool = True,
          order: str | None = "K", ndmin: int = 0) -> Array:
  if order is not None and order != "K":
    raise NotImplementedError("Only implemented for order='K'")

  # check if the given dtype is compatible with JAX
  dtypes.check_user_dtype_supported(dtype, "array")

  # Here we make a judgment call: we only return a weakly-typed array when the
  # input object itself is weakly typed. That ensures asarray(x) is a no-op
  # whenever x is weak, but avoids introducing weak types with something like
  # array([1, 2, 3])
  weak_type = dtype is None and dtypes.is_weakly_typed(object)

  # For Python scalar literals, call coerce_to_array to catch any overflow
  # errors. We don't use dtypes.is_python_scalar because we don't want this
  # triggering for traced values. We do this here because it matters whether or
  # not dtype is None. We don't assign the result because we want the raw object
  # to be used for type inference below.
  if isinstance(object, (bool, int, float, complex)):
    _ = dtypes.coerce_to_array(object, dtype)

  if hasattr(object, '__jax_array__'):
    object = object.__jax_array__()
  object = tree_map(lambda leaf: leaf.__jax_array__() if hasattr(leaf, "__jax_array__") else leaf,
                    object)
  leaves = tree_leaves(object)
  if dtype is None:
    # Use lattice_result_type rather than result_type to avoid canonicalization.
    # Otherwise, weakly-typed inputs would have their dtypes canonicalized.
    try:
      dtype = dtypes._lattice_result_type(*leaves)[0] if leaves else dtypes.float_
    except TypeError:
      # This happens if, e.g. one of the entries is a memoryview object.
      # This is rare, so we only handle it if the normal path fails.
      leaves = [_convert_to_array_if_dtype_fails(leaf) for leaf in leaves]
      dtype = dtypes._lattice_result_type(*leaves)[0]

  if not weak_type:
    dtype = dtypes.canonicalize_dtype(dtype, allow_extended_dtype=True)

  out: ArrayLike

  if all(not isinstance(leaf, Array) for leaf in leaves):
    # TODO(jakevdp): falling back to numpy here fails to overflow for lists
    # containing large integers; see discussion in
    # https://github.com/google/jax/pull/6047. More correct would be to call
    # coerce_to_array on each leaf, but this may have performance implications.
    out = np.array(object, dtype=dtype, ndmin=ndmin, copy=False)  # type: ignore[arg-type]
  elif isinstance(object, Array):
    assert object.aval is not None
    out = _array_copy(object) if copy else object
  elif isinstance(object, (list, tuple)):
    if object:
      out = stack([asarray(elt, dtype=dtype) for elt in object])
    else:
      out = np.array([], dtype=dtype)  # type: ignore[arg-type]
  else:
    try:
      view = memoryview(object)
    except TypeError:
      pass  # `object` does not support the buffer interface.
    else:
      return array(np.asarray(view), dtype, copy, ndmin=ndmin)

    raise TypeError(f"Unexpected input type for array: {type(object)}")

  out_array: Array = lax_internal._convert_element_type(out, dtype, weak_type=weak_type)
  if ndmin > ndim(out_array):
    out_array = lax.expand_dims(out_array, range(ndmin - ndim(out_array)))
  return out_array
