def _compute_newshape(a: ArrayLike, newshape: Union[DimSize, Shape]) -> Shape:
  """Fixes a -1 value in newshape, if present."""
  # other errors, like having more than one -1, are caught downstream, in
  # reshape_shape_rule.
  try:
    iter(newshape)  # type: ignore[arg-type]
  except:
    newshape = [newshape]
  newshape = core.canonicalize_shape(newshape)  # type: ignore[arg-type]
  neg1s = [i for i, d in enumerate(newshape) if type(d) is int and d == -1]
  if len(neg1s) == 1:
    i, = neg1s
    sz = core.cancel_divide_tracers(np.shape(a), (*newshape[:i], *newshape[i+1:]))
    if sz is not None:
      return (*newshape[:i], sz, *newshape[i+1:])
  return tuple(-core.divide_shape_sizes(np.shape(a), newshape)
               if core.definitely_equal(d, -1) else d
               for d in newshape)
