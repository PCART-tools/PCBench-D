@util._wraps(np.choose, skip_params=['out'])
def choose(a: ArrayLike, choices: Sequence[ArrayLike],
           out: None = None, mode: str = 'raise') -> Array:
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.choose is not supported.")
  util.check_arraylike('choose', a, *choices)
  if not issubdtype(_dtype(a), integer):
    raise ValueError("`a` array must be integer typed")
  N = len(choices)

  if mode == 'raise':
    arr: Array = core.concrete_or_error(asarray, a,
      "The error occurred because jnp.choose was jit-compiled"
      " with mode='raise'. Use mode='wrap' or mode='clip' instead.")
    if reductions.any((arr < 0) | (arr >= N)):
      raise ValueError("invalid entry in choice array")
  elif mode == 'wrap':
    arr = asarray(a) % N
  elif mode == 'clip':
    arr = clip(a, 0, N - 1)
  else:
    raise ValueError(f"mode={mode!r} not understood. Must be 'raise', 'wrap', or 'clip'")

  arr, *choices = broadcast_arrays(arr, *choices)
  return array(choices)[(arr,) + indices(arr.shape, sparse=True)]
