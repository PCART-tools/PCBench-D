@util._wraps(np.flatnonzero, lax_description=_NONZERO_DOC, extra_params=_NONZERO_EXTRA_PARAMS)
def flatnonzero(a: ArrayLike, *, size: Optional[int] = None,
                fill_value: Union[None, ArrayLike, Tuple[ArrayLike]] = None) -> Array:
  return nonzero(ravel(a), size=size, fill_value=fill_value)[0]
