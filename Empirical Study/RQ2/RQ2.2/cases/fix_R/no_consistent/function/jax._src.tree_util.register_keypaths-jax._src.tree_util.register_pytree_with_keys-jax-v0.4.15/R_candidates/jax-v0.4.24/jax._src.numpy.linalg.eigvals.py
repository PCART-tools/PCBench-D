@implements(np.linalg.eigvals)
@jit
def eigvals(a: ArrayLike) -> Array:
  check_arraylike("jnp.linalg.eigvals", a)
  return lax_linalg.eig(a, compute_left_eigenvectors=False,
                        compute_right_eigenvectors=False)[0]
