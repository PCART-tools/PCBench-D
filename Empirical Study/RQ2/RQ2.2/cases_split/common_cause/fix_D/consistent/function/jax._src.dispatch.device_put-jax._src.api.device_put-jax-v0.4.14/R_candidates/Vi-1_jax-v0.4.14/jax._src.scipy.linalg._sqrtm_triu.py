@jit
def _sqrtm_triu(T: Array) -> Array:
  """
  Implements Björck, Å., & Hammarling, S. (1983).
      "A Schur method for the square root of a matrix". Linear algebra and
      its applications", 52, 127-140.
  """
  diag = jnp.sqrt(jnp.diag(T))
  n = diag.size
  U = jnp.diag(diag)

  def i_loop(l, data):
    j, U = data
    i = j - 1 - l
    s = lax.fori_loop(i + 1, j, lambda k, val: val + U[i, k] * U[k, j], 0.0)
    value = jnp.where(T[i, j] == s, 0.0,
                      (T[i, j] - s) / (diag[i] + diag[j]))
    return j, U.at[i, j].set(value)

  def j_loop(j, U):
    _, U = lax.fori_loop(0, j, i_loop, (j, U))
    return U

  U = lax.fori_loop(0, n, j_loop, U)
  return U
