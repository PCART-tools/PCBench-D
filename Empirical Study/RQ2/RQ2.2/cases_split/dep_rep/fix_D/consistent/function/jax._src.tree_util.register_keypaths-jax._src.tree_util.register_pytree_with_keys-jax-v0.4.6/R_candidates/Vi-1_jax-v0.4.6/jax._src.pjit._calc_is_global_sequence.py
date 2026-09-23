def _calc_is_global_sequence(in_positional_semantics, in_shardings):
  if config.jax_array:
    return (True,) * len(in_positional_semantics)
  return tuple((ips == pxla._PositionalSemantics.GLOBAL or
                pxla.is_op_sharding_replicated(i._op_sharding))
               for ips, i in safe_zip(in_positional_semantics, in_shardings))
