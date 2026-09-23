class SVDResult(NamedTuple):
  U: jax.Array
  S: jax.Array
  Vh: jax.Array
