@util._wraps(np.einsum, lax_description=_EINSUM_DOC, skip_params=['out'])
def einsum(
    subscripts, /,
    *operands,
    out: None = None,
    optimize: str = "optimal",
    precision: PrecisionLike = None,
    preferred_element_type: Optional[DTypeLike] = None,
    _use_xeinsum: bool = False,
    _dot_general: Callable[..., Array] = lax.dot_general,
) -> Array:
  operands = (subscripts, *operands)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.einsum is not supported.")

  spec = operands[0] if isinstance(operands[0], str) else None

  if (_use_xeinsum or spec is not None and '{' in spec):
    return jax.named_call(lax.xeinsum, name=spec)(*operands)

  optimize = 'optimal' if optimize is True else optimize
  # using einsum_call=True here is an internal api for opt_einsum

  # Allow handling of shape polymorphism
  non_constant_dim_types = {
      type(d) for op in operands if not isinstance(op, str)
      for d in np.shape(op) if not core.is_constant_dim(d)
  }
  if not non_constant_dim_types:
    contract_path = opt_einsum.contract_path
  else:
    ty = next(iter(non_constant_dim_types))
    contract_path = _poly_einsum_handlers.get(ty, _default_poly_einsum_handler)
  operands, contractions = contract_path(
        *operands, einsum_call=True, use_blas=True, optimize=optimize)

  contractions = tuple((a, frozenset(b), c) for a, b, c, *_ in contractions)

  _einsum_computation = jax.named_call(
      _einsum, name=spec) if spec is not None else _einsum
  return _einsum_computation(operands, contractions, precision,  # type: ignore[operator]
                             preferred_element_type, _dot_general)
