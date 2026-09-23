@_wraps(np.linalg.eig, lax_description="""
This differs from :func:`numpy.linalg.eig` in that the return type of
:func:`jax.numpy.linalg.eig` is always ``complex64`` for 32-bit input,
and ``complex128`` for 64-bit input.

At present, non-symmetric eigendecomposition is only implemented on the CPU
backend. However eigendecomposition for symmetric/Hermitian matrices is
implemented more widely (see :func:`jax.numpy.linalg.eigh`).
""")
def eig(a):
  a, = _promote_dtypes_inexact(jnp.asarray(a))
  return lax_linalg.eig(a, compute_left_eigenvectors=False)
