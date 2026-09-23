def _solve_P_Q(P: ArrayLike, Q: ArrayLike, upper_triangular: bool = False) -> Array:
  if upper_triangular:
    return solve_triangular(Q, P)
  else:
    return jnp.linalg.solve(Q, P)
