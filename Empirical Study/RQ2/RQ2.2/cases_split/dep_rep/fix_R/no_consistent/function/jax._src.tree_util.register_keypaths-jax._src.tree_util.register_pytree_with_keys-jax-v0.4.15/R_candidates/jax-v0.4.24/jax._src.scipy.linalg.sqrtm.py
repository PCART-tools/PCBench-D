@implements(scipy.linalg.sqrtm,
        lax_description="""
This differs from ``scipy.linalg.sqrtm`` in that the return type of
``jax.scipy.linalg.sqrtm`` is always ``complex64`` for 32-bit input,
and ``complex128`` for 64-bit input.

This function implements the complex Schur method described in [A]. It does not use recursive blocking
to speed up computations as a Sylvester Equation solver is not available yet in JAX.

[A] Björck, Å., & Hammarling, S. (1983).
    "A Schur method for the square root of a matrix". Linear algebra and its applications, 52, 127-140.
""")
def sqrtm(A: ArrayLike, blocksize: int = 1) -> Array:
  if blocksize > 1:
      raise NotImplementedError("Blocked version is not implemented yet.")
  return _sqrtm(A)
