@_wraps(np.ravel, lax_description=_ARRAY_VIEW_DOC)
@partial(jit, static_argnames=('order',), inline=True)
def ravel(a, order="C"):
  _stackable(a) or _check_arraylike("ravel", a)
  if order == "K":
    raise NotImplementedError("Ravel not implemented for order='K'.")
  return reshape(a, (size(a),), order)
