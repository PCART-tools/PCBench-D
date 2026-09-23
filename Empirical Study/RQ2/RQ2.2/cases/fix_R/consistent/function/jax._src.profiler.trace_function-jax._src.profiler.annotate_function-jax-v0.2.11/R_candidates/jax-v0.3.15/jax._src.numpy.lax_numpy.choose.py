@_wraps(np.choose, skip_params=['out'])
def choose(a, choices, out=None, mode='raise'):
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.choose is not supported.")
  _check_arraylike('choose', a, *choices)
  if not issubdtype(_dtype(a), integer):
    raise ValueError("`a` array must be integer typed")
  N = len(choices)

  if mode == 'raise':
    a = core.concrete_or_error(asarray, a,
      "The error occurred because jnp.choose was jit-compiled"
      " with mode='raise'. Use mode='wrap' or mode='clip' instead.")
    if any((a < 0) | (a >= N)):
      raise ValueError("invalid entry in choice array")
  elif mode == 'wrap':
    a = a % N
  elif mode == 'clip':
    a = clip(a, 0, N - 1)
  else:
    raise ValueError(f"mode={mode!r} not understood. Must be 'raise', 'wrap', or 'clip'")

  a, *choices = broadcast_arrays(a, *choices)
  return array(choices)[(a,) + indices(a.shape, sparse=True)]
