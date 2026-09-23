def population_count(x: ArrayLike) -> Array:
  r"""Elementwise popcount, count the number of set bits in each element."""
  return population_count_p.bind(x)
