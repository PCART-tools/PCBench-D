def lu_solve(lu: ArrayLike, permutation: ArrayLike, b: ArrayLike,
             trans: int = 0) -> Array:
  """LU solve with broadcasting."""
  return _lu_solve(lu, permutation, b, trans)
