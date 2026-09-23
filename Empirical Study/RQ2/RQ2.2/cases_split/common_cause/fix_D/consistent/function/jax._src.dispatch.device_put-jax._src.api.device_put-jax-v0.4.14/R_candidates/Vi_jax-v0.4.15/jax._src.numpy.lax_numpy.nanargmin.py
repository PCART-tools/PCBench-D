@util._wraps(np.nanargmin, lax_description=_NANARG_DOC.format("min"),  skip_params=['out'])
def nanargmin(
    a: ArrayLike,
    axis: int | None = None,
    out: None = None,
    keepdims: bool | None = None,
) -> Array:
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.nanargmin is not supported.")
  return _nanargmin(a, None if axis is None else operator.index(axis), keepdims=bool(keepdims))
