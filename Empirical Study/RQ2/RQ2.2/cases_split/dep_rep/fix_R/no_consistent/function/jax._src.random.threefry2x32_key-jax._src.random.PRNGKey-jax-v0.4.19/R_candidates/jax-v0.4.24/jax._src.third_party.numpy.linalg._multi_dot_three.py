def _multi_dot_three(A, B, C, precision):
  """
  Find the best order for three arrays and do the multiplication.
  For three arguments `_multi_dot_three` is approximately 15 times faster
  than `_multi_dot_matrix_chain_order`
  """
  a0, a1b0 = A.shape
  b1c0, c1 = C.shape
  # cost1 = cost((AB)C) = a0*a1b0*b1c0 + a0*b1c0*c1
  cost1 = a0 * b1c0 * (a1b0 + c1)
  # cost2 = cost(A(BC)) = a1b0*b1c0*c1 + a0*a1b0*c1
  cost2 = a1b0 * c1 * (a0 + b1c0)

  if cost1 < cost2:
    return jnp.dot(jnp.dot(A, B, precision=precision), C, precision=precision)
  else:
    return jnp.dot(A, jnp.dot(B, C, precision=precision), precision=precision)
