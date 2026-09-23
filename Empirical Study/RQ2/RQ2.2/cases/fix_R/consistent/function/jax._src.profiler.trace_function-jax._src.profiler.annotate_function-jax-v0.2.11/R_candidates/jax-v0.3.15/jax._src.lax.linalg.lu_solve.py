def lu_solve(lu, permutation, b, trans=0):
  """LU solve with broadcasting."""
  return _lu_solve(lu, permutation, b, trans)
