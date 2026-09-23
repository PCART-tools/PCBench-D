@util.implements(getattr(np, "permute_dims", None))
def permute_dims(a: ArrayLike, /, axes: tuple[int, ...]) -> Array:
  util.check_arraylike("permute_dims", a)
  return lax.transpose(a, axes)
