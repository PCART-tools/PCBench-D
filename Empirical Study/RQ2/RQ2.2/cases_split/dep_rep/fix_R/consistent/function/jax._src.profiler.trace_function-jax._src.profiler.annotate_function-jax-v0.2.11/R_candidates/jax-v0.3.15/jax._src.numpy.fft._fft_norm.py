def _fft_norm(s, func_name, norm):
  if norm == "backward":
    return 1
  elif norm == "ortho":
    return jnp.sqrt(jnp.prod(s)) if func_name.startswith('i') else 1/jnp.sqrt(jnp.prod(s))
  elif norm == "forward":
    return jnp.prod(s) if func_name.startswith('i') else 1/jnp.prod(s)
  raise ValueError(f'Invalid norm value {norm}; should be "backward",'
                    '"ortho" or "forward".')
