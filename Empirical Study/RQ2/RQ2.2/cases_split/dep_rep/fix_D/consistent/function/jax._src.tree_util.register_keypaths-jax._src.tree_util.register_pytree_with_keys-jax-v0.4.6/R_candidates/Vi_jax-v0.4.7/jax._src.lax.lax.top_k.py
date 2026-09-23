def top_k(operand: ArrayLike, k: int) -> Tuple[Array, Array]:
  """Returns top ``k`` values and their indices along the last axis of ``operand``.

  Args:
    operand: N-dimensional array of non-complex type.
    k: integer specifying the number of top entries.

  Returns:
    values: array containing the top k values along the last axis.
    indices: array containing the indices corresponding to values.

  See also:
  - :func:`jax.lax.approx_max_k`
  - :func:`jax.lax.approx_min_k`
  """
  k = int(k)
  if k < 0:
    raise ValueError(f"k argument to top_k must be nonnegative, got {k}")
  return top_k_p.bind(operand, k=k)
