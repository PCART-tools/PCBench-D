def add_jaxvals(x: ArrayLike, y: ArrayLike) -> Array:
  return add_jaxvals_p.bind(x, y)
