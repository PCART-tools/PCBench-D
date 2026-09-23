@util.implements(np.flatnonzero, lax_description=_NONZERO_DOC, extra_params=_NONZERO_EXTRA_PARAMS)
def flatnonzero(a: ArrayLike, *, size: int | None = None,
                fill_value: None | ArrayLike | tuple[ArrayLike] = None) -> Array:
  return nonzero(ravel(a), size=size, fill_value=fill_value)[0]
