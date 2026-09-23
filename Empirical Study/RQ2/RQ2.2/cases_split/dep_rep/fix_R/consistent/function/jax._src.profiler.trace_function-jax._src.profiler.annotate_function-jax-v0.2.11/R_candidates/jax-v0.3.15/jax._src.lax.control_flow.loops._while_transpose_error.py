def _while_transpose_error(*_, **kwargs):
  raise ValueError("Reverse-mode differentiation does not work for "
                   "lax.while_loop or lax.fori_loop. "
                   "Try using lax.scan instead.")
