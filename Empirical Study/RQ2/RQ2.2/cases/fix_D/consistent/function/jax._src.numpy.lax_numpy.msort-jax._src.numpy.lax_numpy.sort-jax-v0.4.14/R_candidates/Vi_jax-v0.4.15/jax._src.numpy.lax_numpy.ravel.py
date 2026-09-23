@util._wraps(np.ravel, lax_description=_ARRAY_VIEW_DOC)
@partial(jit, static_argnames=('order',), inline=True)
def ravel(a: ArrayLike, order: str = "C") -> Array:
  util.check_arraylike("ravel", a)
  if order == "K":
    raise NotImplementedError("Ravel not implemented for order='K'.")
  return reshape(a, (size(a),), order)
