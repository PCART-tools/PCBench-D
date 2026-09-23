def _compute_newshape(a, newshape):
  """Fixes a -1 value in newshape, if present."""
  # other errors, like having more than one -1, are caught downstream, in
  # reshape_shape_rule.
  try: iter(newshape)
  except: iterable = False
  else: iterable = True
  newshape = core.canonicalize_shape(newshape if iterable else [newshape])
  return tuple(- core.divide_shape_sizes(np.shape(a), newshape)
               if core.symbolic_equal_dim(d, -1) else d
               for d in newshape)
