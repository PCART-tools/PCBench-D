@util.implements(np.array, lax_description=_ARRAY_DOC, extra_params="""
device: (optional) :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
  to which the created array will be committed.
""")
def array(object: Any, dtype: DTypeLike | None = None, copy: bool = True,
          order: str | None = "K", ndmin: int = 0,
          *, device: xc.Device | Sharding | None = None) -> Array:
  if order is not None and order != "K":
    raise NotImplementedError("Only implemented for order='K'")

  # check if the given dtype is compatible with JAX
  dtypes.check_user_dtype_supported(dtype, "array")

  # Here we make a judgment call: we only return a weakly-typed array when the
  # input object itself is weakly typed. That ensures asarray(x) is a no-op
  # whenever x is weak, but avoids introducing weak types with something like
  # array([1, 2, 3])
  weak_type = dtype is None and dtypes.is_weakly_typed(object)
  sharding = canonicalize_device_to_sharding(device)

  # Use device_put to avoid a copy for ndarray inputs.
  if (not copy and isinstance(object, np.ndarray) and
      (dtype is None or dtype == object.dtype) and (ndmin <= object.ndim) and
      device is None):
    # Keep the output uncommitted.
    return jax.device_put(object)

  # For Python scalar literals, call coerce_to_array to catch any overflow
  # errors. We don't use dtypes.is_python_scalar because we don't want this
  # triggering for traced values. We do this here because it matters whether or
  # not dtype is None. We don't assign the result because we want the raw object
  # to be used for type inference below.
  if isinstance(object, (bool, int, float, complex)):
    _ = dtypes.coerce_to_array(object, dtype)
  elif not isinstance(object, Array):
    # Check if object supports any of the data exchange protocols
    # (except dlpack, see data-apis/array-api#301). If it does,
    # consume the object as jax array and continue (but not return) so
    # that other array() arguments get processed against the input
    # object.
    #
    # Notice that data exchange protocols define dtype in the
    # corresponding data structures and it may not be available as
    # object.dtype. So, we'll resolve the protocols here before
    # evaluating object.dtype.
    if hasattr(object, '__jax_array__'):
      object = object.__jax_array__()
    elif hasattr(object, '__cuda_array_interface__'):
      cai = object.__cuda_array_interface__
      backend = xla_bridge.get_backend("cuda")
      if cuda_plugin_extension is None:
        device_id = None
      else:
        device_id = cuda_plugin_extension.get_device_ordinal(cai["data"][0])
      object = xc._xla.cuda_array_interface_to_buffer(
          cai=cai, gpu_backend=backend, device_id=device_id)

  object = tree_map(lambda leaf: leaf.__jax_array__()
                    if hasattr(leaf, "__jax_array__") else leaf, object)
  leaves = tree_leaves(object, is_leaf=lambda x: x is None)
  if any(leaf is None for leaf in leaves):
    # Added Nov 16 2023
    if deprecations.is_accelerated("jax-numpy-array-none"):
      raise TypeError("None is not a valid value for jnp.array")
    warnings.warn(
      "None encountered in jnp.array(); this is currently treated as NaN. "
      "In the future this will result in an error.",
      FutureWarning, stacklevel=2)
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
    dtype = dtypes.canonicalize_dtype(dtype, allow_extended_dtype=True)  # type: ignore[assignment]

  out: ArrayLike

  if all(not isinstance(leaf, Array) for leaf in leaves):
    # TODO(jakevdp): falling back to numpy here fails to overflow for lists
    # containing large integers; see discussion in
    # https://github.com/google/jax/pull/6047. More correct would be to call
    # coerce_to_array on each leaf, but this may have performance implications.
    out = np.asarray(object, dtype=dtype)
  elif isinstance(object, Array):
    assert object.aval is not None
    out = _array_copy(object) if copy else object
  elif isinstance(object, (list, tuple)):
    if object:
      out = stack([asarray(elt, dtype=dtype) for elt in object])
    else:
      out = np.array([], dtype=dtype)
  elif _supports_buffer_protocol(object):
    object = memoryview(object)
    # TODO(jakevdp): update this once we support NumPy 2.0 semantics for the copy arg.
    out = np.array(object) if copy else np.asarray(object)
  else:
    raise TypeError(f"Unexpected input type for array: {type(object)}")
  out_array: Array = lax_internal._convert_element_type(
      out, dtype, weak_type=weak_type, sharding=sharding)
  if ndmin > ndim(out_array):
    out_array = lax.expand_dims(out_array, range(ndmin - ndim(out_array)))
  return out_array
