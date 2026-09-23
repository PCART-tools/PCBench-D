@_wraps(np.einsum, lax_description=_EINSUM_DOC, skip_params=['out'])
def einsum(*operands, out=None, optimize='optimal', precision=None,
           _use_xeinsum=False):
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.einsum is not supported.")

  if (_use_xeinsum or isinstance(operands[0], str) and '{' in operands[0]):
    return lax.xeinsum(*operands)

  optimize = 'optimal' if optimize is True else optimize
  # using einsum_call=True here is an internal api for opt_einsum

  # Allow handling of shape polymorphism
  non_constant_dim_types = {
      type(d) for op in operands if not isinstance(op, str)
      for d in np.shape(op) if not core.is_constant_dim(d)
  }
  if not non_constant_dim_types:
    einsum_contract_path_fn = opt_einsum.contract_path
  else:
    einsum_contract_path_fn = _polymorphic_einsum_contract_path_handlers[next(iter(non_constant_dim_types))]
  operands, contractions = einsum_contract_path_fn(
        *operands, einsum_call=True, use_blas=True, optimize=optimize)

  contractions = tuple((a, frozenset(b), c) for a, b, c, *_ in contractions)
  return _einsum(operands, contractions, precision)
