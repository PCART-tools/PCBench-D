def _dot_general_batch_dim_nums(ndims, batch_dims, dimension_numbers):
  # there are three kinds of dimensions in a dot_general:
  # - contraction dimensions appear in lhs and rhs but not the result
  # - batch dimensions appear in lhs, rhs, and result
  # - tensor product dimensions appear in the result and one of lhs or rhs
  lhs_ndim, rhs_ndim = ndims
  lbd, rbd = batch_dims
  assert lbd is not None or rbd is not None
  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers

  def bump_dims(dims, b):
    return tuple(np.add(dims, np.greater_equal(dims, b)))

  if lbd is not None and rbd is not None:
    # adding a batch dimension
    lhs_batch = (lbd,) + bump_dims(lhs_batch, lbd)
    rhs_batch = (rbd,) + bump_dims(rhs_batch, rbd)
    lhs_contract = bump_dims(lhs_contract, lbd)
    rhs_contract = bump_dims(rhs_contract, rbd)
    result_batch_dim = 0
  else:
    # adding a tensor product dimension
    if lbd is not None:
      other = tuple(d for d in range(lhs_ndim)
                    if d not in lhs_batch and d not in lhs_contract)
      result_batch_dim = (len(lhs_batch) + sum(np.less(other, lbd)))
      lhs_batch = bump_dims(lhs_batch, lbd)
      lhs_contract = bump_dims(lhs_contract, lbd)
    else:
      other = tuple(d for d in range(rhs_ndim)
                    if d not in rhs_batch and d not in rhs_contract)
      result_batch_dim = (lhs_ndim - len(lhs_contract) +
                          sum(np.less(other, rbd)))
      rhs_batch = bump_dims(rhs_batch, rbd)
      rhs_contract = bump_dims(rhs_contract, rbd)

  new_dimension_numbers = ((lhs_contract, rhs_contract), (lhs_batch, rhs_batch))
  return new_dimension_numbers, int(result_batch_dim)
