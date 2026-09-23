def _compute_newshape(a: ArrayLike, newshape: Union[DimSize, Shape]) -> Shape:
  """Fixes a -1 value in newshape, if present."""
  # other errors, like having more than one -1, are caught downstream, in
  # reshape_shape_rule.
  try:
    iter(newshape)  # type: ignore[arg-type]
  except:
    iterable = False
  else:
    iterable = True
  newshape = core.canonicalize_shape(newshape if iterable else [newshape])  # type: ignore[arg-type]
  return tuple(- core.divide_shape_sizes(np.shape(a), newshape)
               if core.symbolic_equal_dim(d, -1) else d
               for d in newshape)
