@util.implements(np.fill_diagonal, lax_description="""
The semantics of :func:`numpy.fill_diagonal` is to modify arrays in-place, which
JAX cannot do because JAX arrays are immutable. Thus :func:`jax.numpy.fill_diagonal`
adds the ``inplace`` parameter, which must be set to ``False`` by the user as a
reminder of this API difference.
""", extra_params="""
inplace : bool, default=True
    If left to its default value of True, JAX will raise an error. This is because
    the semantics of :func:`numpy.fill_diagonal` are to modify the array in-place,
    which is not possible in JAX due to the immutability of JAX arrays.
""")
def fill_diagonal(a: ArrayLike, val: ArrayLike, wrap: bool = False, *, inplace: bool = True) -> Array:
  if inplace:
    raise NotImplementedError("JAX arrays are immutable, must use inplace=False")
  if wrap:
    raise NotImplementedError("wrap=True is not implemented, must use wrap=False")
  util.check_arraylike("fill_diagonal", a, val)
  a = asarray(a)
  val = asarray(val)
  if a.ndim < 2:
    raise ValueError("array must be at least 2-d")
  if a.ndim > 2 and not all(n == a.shape[0] for n in a.shape[1:]):
    raise ValueError("All dimensions of input must be of equal length")
  n = min(a.shape)
  idx = diag_indices(n, a.ndim)
  return a.at[idx].set(val if val.ndim == 0 else _tile_to_size(val.ravel(), n))
