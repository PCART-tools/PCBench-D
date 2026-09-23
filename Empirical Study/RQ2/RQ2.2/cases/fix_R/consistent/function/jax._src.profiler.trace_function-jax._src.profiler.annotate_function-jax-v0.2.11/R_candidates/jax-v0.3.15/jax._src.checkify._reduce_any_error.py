def _reduce_any_error(errs, codes, payloads):
  reduced_idx = jnp.argsort(errs)[-1]
  return errs[reduced_idx], codes[reduced_idx], payloads[reduced_idx]
