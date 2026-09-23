def _nearest_indices_and_weights(coordinate: Array) -> List[Tuple[Array, ArrayLike]]:
  index = _round_half_away_from_zero(coordinate).astype(jnp.int32)
  weight = coordinate.dtype.type(1)
  return [(index, weight)]
