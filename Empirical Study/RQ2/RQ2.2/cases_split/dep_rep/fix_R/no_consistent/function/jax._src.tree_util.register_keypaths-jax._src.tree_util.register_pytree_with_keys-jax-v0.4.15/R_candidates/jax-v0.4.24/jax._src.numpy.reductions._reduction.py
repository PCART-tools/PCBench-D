def _reduction(a: ArrayLike, name: str, np_fun: Any, op: ReductionOp, init_val: ArrayLike,
               *, has_identity: bool = True,
               preproc: Callable[[ArrayLike], ArrayLike] | None = None,
               bool_op: ReductionOp | None = None,
               upcast_f16_for_computation: bool = False,
               axis: Axis = None, dtype: DTypeLike | None = None, out: None = None,
               keepdims: bool = False, initial: ArrayLike | None = None,
               where_: ArrayLike | None = None,
               parallel_reduce: Callable[..., Array] | None = None,
               promote_integers: bool = False) -> Array:
  bool_op = bool_op or op
  # Note: we must accept out=None as an argument, because numpy reductions delegate to
  # object methods. For example `np.sum(x)` will call `x.sum()` if the `sum()` method
  # exists, passing along all its arguments.
  if out is not None:
    raise NotImplementedError(f"The 'out' argument to jnp.{name} is not supported.")
  check_arraylike(name, a)
  dtypes.check_user_dtype_supported(dtype, name)
  axis = core.concrete_or_error(None, axis, f"axis argument to jnp.{name}().")

  if initial is None and not has_identity and where_ is not None:
    raise ValueError(f"reduction operation {name} does not have an identity, so to use a "
                     f"where mask one has to specify 'initial'")

  a = a if isinstance(a, Array) else lax_internal.asarray(a)
  a = preproc(a) if preproc else a
  pos_dims, dims = _reduction_dims(a, axis)

  if initial is None and not has_identity:
    shape = np.shape(a)
    if not _all(shape[d] >= 1 for d in pos_dims):
      raise ValueError(f"zero-size array to reduction operation {name} which has no identity")

  result_dtype = dtype or dtypes.dtype(a)

  if dtype is None and promote_integers:
    # Note: NumPy always promotes to 64-bit; jax instead promotes to the
    # default dtype as defined by dtypes.int_ or dtypes.uint.
    if dtypes.issubdtype(result_dtype, np.bool_):
      result_dtype = dtypes.int_
    elif dtypes.issubdtype(result_dtype, np.unsignedinteger):
      if np.iinfo(result_dtype).bits < np.iinfo(dtypes.uint).bits:
        result_dtype = dtypes.uint
    elif dtypes.issubdtype(result_dtype, np.integer):
      if np.iinfo(result_dtype).bits < np.iinfo(dtypes.int_).bits:
        result_dtype = dtypes.int_

  result_dtype = dtypes.canonicalize_dtype(result_dtype)

  if upcast_f16_for_computation and dtypes.issubdtype(result_dtype, np.inexact):
    computation_dtype = _upcast_f16(result_dtype)
  else:
    computation_dtype = result_dtype
  a = lax.convert_element_type(a, computation_dtype)
  op = op if computation_dtype != np.bool_ else bool_op
  # NB: in XLA, init_val must be an identity for the op, so the user-specified
  # initial value must be applied afterward.
  init_val = _reduction_init_val(a, init_val)
  if where_ is not None:
    a = _where(where_, a, init_val)
  if pos_dims is not dims:
    if parallel_reduce is None:
      raise NotImplementedError(f"Named reductions not implemented for jnp.{name}()")
    result = parallel_reduce(a, dims)
  else:
    result = lax.reduce(a, init_val, op, dims)
  if initial is not None:
    initial_arr = lax.convert_element_type(initial, lax_internal.asarray(a).dtype)
    if initial_arr.shape != ():
      raise ValueError("initial value must be a scalar. "
                       f"Got array of shape {initial_arr.shape}")
    result = op(initial_arr, result)
  if keepdims:
    result = lax.expand_dims(result, pos_dims)
  return lax.convert_element_type(result, dtype or result_dtype)
