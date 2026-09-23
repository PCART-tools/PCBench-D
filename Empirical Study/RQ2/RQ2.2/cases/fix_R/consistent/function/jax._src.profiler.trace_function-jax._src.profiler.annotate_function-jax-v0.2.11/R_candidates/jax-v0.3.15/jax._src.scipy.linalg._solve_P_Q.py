def _solve_P_Q(P, Q, upper_triangular=False):
  if upper_triangular:
    return solve_triangular(Q, P)
  else:
    return np_linalg.solve(Q, P)
