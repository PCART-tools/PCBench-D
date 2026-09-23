def _lu_pivots_to_permutation_abstract_eval(pivots, *, permutation_size):
  pivots = raise_to_shaped(pivots)
  if isinstance(pivots, ShapedArray):
    if pivots.ndim < 1 or pivots.dtype != np.dtype(np.int32):
      raise ValueError(
          'Argument to lu_pivots_to_permutation must have rank >= 1 and dtype '
          'int32. Got shape={} and dtype={}'.format(pivots.shape, pivots.dtype))

    if permutation_size < pivots.shape[-1]:
      raise ValueError(
          'Output permutation size {} has to exceed the trailing dimension of '
          'the pivots. Got shape {}'.format(permutation_size, pivots.shape))

    batch_dims = pivots.shape[:-1]
    permutations = pivots.update(shape=batch_dims + (permutation_size,))
  else:
    permutations = pivots

  return permutations
