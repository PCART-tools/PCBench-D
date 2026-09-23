def add_jaxvals(x: ArrayLike, y: ArrayLike) -> Array:
  dtype = core.get_aval(x).dtype
  return add_jaxvals_p.bind(x, y)
