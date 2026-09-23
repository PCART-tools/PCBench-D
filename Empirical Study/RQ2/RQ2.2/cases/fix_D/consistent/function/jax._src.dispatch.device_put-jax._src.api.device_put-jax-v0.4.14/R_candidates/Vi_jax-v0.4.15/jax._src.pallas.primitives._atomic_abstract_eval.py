def _atomic_abstract_eval(ref_aval, val_aval, *all_avals,
                          args_tree, atomic_type: AtomicOpType,
                          **_: Any):
  if ref_aval.dtype == jnp.dtype("float16") and atomic_type != AtomicOpType.ADD:
    raise ValueError(f"`atomic_{atomic_type.value}` does not support f16.")
  if ref_aval.dtype in {jnp.dtype("bool"), jnp.dtype("int8"),
                        jnp.dtype("int16"), jnp.bfloat16}:
    raise ValueError(f"`atomic_{atomic_type.value}` does not support {ref_aval.dtype}.")
  return _swap_abstract_eval(ref_aval, val_aval, *all_avals,
                             args_tree=args_tree)
