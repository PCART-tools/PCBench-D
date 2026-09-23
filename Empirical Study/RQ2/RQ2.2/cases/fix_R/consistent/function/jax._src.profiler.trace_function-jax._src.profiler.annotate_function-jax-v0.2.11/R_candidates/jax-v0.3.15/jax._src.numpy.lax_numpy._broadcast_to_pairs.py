def _broadcast_to_pairs(nvals, nd, name):
  nvals = np.asarray(tree_map(
    lambda x: core.concrete_or_error(np.array, x, context=f"{name} argument of jnp.pad"),
    nvals))
  if nvals.dtype.kind == 'O':
    raise TypeError(f'`{name}` entries must be the same shape.')

  if nvals.shape == (nd, 2):
    # ((before_1, after_1), ..., (before_N, after_N))
    return tuple(tuple(nval) for nval in nvals)
  elif nvals.shape == (1, 2):
    # ((before, after),)
    return tuple(tuple(nvals[0]) for i in range(nd))
  elif nvals.shape == (2,):
    # (before, after)  (not in the numpy docstring but works anyway)
    return tuple(tuple(nvals) for i in range(nd))
  elif nvals.shape == (1,):
    # (pad,)
    return tuple((nvals[0], nvals[0]) for i in range(nd))
  elif nvals.shape == ():
    # pad
    return tuple((nvals.flat[0], nvals.flat[0]) for i in range(nd))
  else:
    raise ValueError(f"jnp.pad: {name} with nd={nd} has unsupported shape {nvals.shape}. "
                     f"Valid shapes are ({nd}, 2), (1, 2), (2,), (1,), or ().")
