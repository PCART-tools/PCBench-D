@partial(jit, static_argnames=('trans', 'lower', 'unit_diagonal'))
def _solve_triangular(a, b, trans, lower, unit_diagonal):
  if trans == 0 or trans == "N":
    transpose_a, conjugate_a = False, False
  elif trans == 1 or trans == "T":
    transpose_a, conjugate_a = True, False
  elif trans == 2 or trans == "C":
    transpose_a, conjugate_a = True, True
  else:
    raise ValueError(f"Invalid 'trans' value {trans}")

  a, b = _promote_dtypes_inexact(jnp.asarray(a), jnp.asarray(b))

  # lax_linalg.triangular_solve only supports matrix 'b's at the moment.
  b_is_vector = jnp.ndim(a) == jnp.ndim(b) + 1
  if b_is_vector:
    b = b[..., None]
  out = lax_linalg.triangular_solve(a, b, left_side=True, lower=lower,
                                    transpose_a=transpose_a,
                                    conjugate_a=conjugate_a,
                                    unit_diagonal=unit_diagonal)
  if b_is_vector:
    return out[..., 0]
  else:
    return out
