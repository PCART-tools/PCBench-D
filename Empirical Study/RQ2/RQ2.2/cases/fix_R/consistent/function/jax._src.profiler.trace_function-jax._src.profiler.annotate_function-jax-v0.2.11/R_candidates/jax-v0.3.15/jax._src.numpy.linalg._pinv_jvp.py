@pinv.defjvp
def _pinv_jvp(rcond, primals, tangents):
  # The Differentiation of Pseudo-Inverses and Nonlinear Least Squares Problems
  # Whose Variables Separate. Author(s): G. H. Golub and V. Pereyra. SIAM
  # Journal on Numerical Analysis, Vol. 10, No. 2 (Apr., 1973), pp. 413-432.
  # (via https://en.wikipedia.org/wiki/Moore%E2%80%93Penrose_inverse#Derivative)
  a, = primals
  a_dot, = tangents
  p = pinv(a, rcond=rcond)
  m, n = a.shape[-2:]
  # TODO(phawkins): on TPU, we would need to opt into high precision here.
  # TODO(phawkins): consider if this can be simplified in the Hermitian case.
  p_dot = -p @ a_dot @ p
  I_n = lax.expand_dims(jnp.eye(m, dtype=a.dtype), range(a.ndim - 2))
  p_dot = p_dot + p @ _H(p) @ _H(a_dot) @ (I_n - a @ p)
  I_m = lax.expand_dims(jnp.eye(n, dtype=a.dtype), range(a.ndim - 2))
  p_dot = p_dot + (I_m - p @ a) @ _H(a_dot) @ _H(p) @ p
  return p, p_dot
