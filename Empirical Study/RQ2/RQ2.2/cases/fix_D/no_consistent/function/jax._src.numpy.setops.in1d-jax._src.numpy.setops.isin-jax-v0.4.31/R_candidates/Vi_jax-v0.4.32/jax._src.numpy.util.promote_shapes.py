def promote_shapes(fun_name: str, *args: ArrayLike) -> list[Array]:
  """Apply NumPy-style broadcasting, making args shape-compatible for lax.py."""
  if len(args) < 2:
    return [lax.asarray(arg) for arg in args]
  else:
    shapes = [np.shape(arg) for arg in args]
    if config.dynamic_shapes.value:
      # With dynamic shapes we don't support singleton-dimension broadcasting;
      # we instead broadcast out to the full shape as a temporary workaround.
      # TODO(mattjj): revise this workaround
      res_shape = lax.broadcast_shapes(*shapes)  # Can raise an error!
      return [_broadcast_to(arg, res_shape) for arg, shp in zip(args, shapes)]
    else:
      if all(len(shapes[0]) == len(s) for s in shapes[1:]):
        return [lax.asarray(arg) for arg in args]  # no need for rank promotion, so rely on lax promotion
      nonscalar_ranks = {len(shp) for shp in shapes if shp}
      if len(nonscalar_ranks) < 2:
        return [lax.asarray(arg) for arg in args]  # rely on lax scalar promotion
      else:
        if config.numpy_rank_promotion.value != "allow":
          _rank_promotion_warning_or_error(fun_name, shapes)
        result_rank = len(lax.broadcast_shapes(*shapes))
        return [lax.broadcast_to_rank(arg, result_rank) for arg in args]
