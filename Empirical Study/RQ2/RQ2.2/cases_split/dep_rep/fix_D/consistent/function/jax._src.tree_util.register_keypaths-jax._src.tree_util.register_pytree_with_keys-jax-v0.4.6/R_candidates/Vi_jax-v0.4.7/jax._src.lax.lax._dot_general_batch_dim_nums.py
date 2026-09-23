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

  if type(lbd) is type(rbd) is int:
    # adding a batch dimension
    lhs_batch = (lbd,) + bump_dims(lhs_batch, lbd)
    rhs_batch = (rbd,) + bump_dims(rhs_batch, rbd)
    lhs_contract = bump_dims(lhs_contract, lbd)
    rhs_contract = bump_dims(rhs_contract, rbd)
    result_batch_dim = 0
  elif rbd is None and type(lbd) is ConcatAxis and lbd.axis not in lhs_contract:
    if lbd.axis in lhs_batch:
      axis = int(np.sum(np.less(lhs_batch, lbd.axis)))
    else:
      lhs_tensor = [d for d in range(lhs_ndim)
                    if d not in lhs_batch and d not in lhs_contract]
      axis = len(lhs_batch) + int(np.sum(np.less(lhs_tensor, lbd.axis)))
    result_batch_dim = ConcatAxis(axis, lbd.segment_lengths)
  elif lbd is None and type(rbd) is ConcatAxis and rbd.axis not in rhs_contract:
    if rbd.axis in rhs_batch:
      axis = int(np.sum(np.less(rhs_batch, rbd.axis)))
    else:
      rhs_tensor = [d for d in range(rhs_ndim)
                    if d not in rhs_batch and d not in rhs_contract]
      axis = (lhs_ndim - len(lhs_contract) +
              int(sum(np.less(rhs_tensor, rbd.axis))))
    result_batch_dim = ConcatAxis(axis, rbd.segment_lengths)
  elif (type(lbd) is int and
        (rbd is None or type(rbd) is ConcatAxis and
         rbd.axis not in rhs_contract)):
    lhs_tensor = [d for d in range(lhs_ndim)
                  if d not in lhs_batch and d not in lhs_contract]
    result_batch_dim = len(lhs_batch) + int(sum(np.less(lhs_tensor, lbd)))
    lhs_batch = bump_dims(lhs_batch, lbd)
    lhs_contract = bump_dims(lhs_contract, lbd)
  elif (type(rbd) is int and
        (lbd is None or type(lbd) is ConcatAxis and
         lbd.axis not in lhs_contract)):
    rhs_tensor = [d for d in range(rhs_ndim)
                  if d not in rhs_batch and d not in rhs_contract]
    result_batch_dim = (lhs_ndim - len(lhs_contract) +
                        int(sum(np.less(rhs_tensor, rbd))))
    rhs_batch = bump_dims(rhs_batch, rbd)
    rhs_contract = bump_dims(rhs_contract, rbd)
  else:
    assert False

  new_dimension_numbers = ((lhs_contract, rhs_contract), (lhs_batch, rhs_batch))
  return new_dimension_numbers, result_batch_dim
