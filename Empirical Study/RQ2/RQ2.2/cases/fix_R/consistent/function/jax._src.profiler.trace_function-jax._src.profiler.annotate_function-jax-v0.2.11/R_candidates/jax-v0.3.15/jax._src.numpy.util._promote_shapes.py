def _promote_shapes(fun_name, *args):
  """Apply NumPy-style broadcasting, making args shape-compatible for lax.py."""
  if len(args) < 2:
    return args
  else:
    shapes = [np.shape(arg) for arg in args]
    if config.jax_dynamic_shapes:
      # With dynamic shapes we don't support singleton-dimension broadcasting;
      # we instead broadcast out to the full shape as a temporary workaround.
      # TODO(mattjj): revise this workaround
      res_shape = lax.broadcast_shapes(*shapes)  # Can raise an error!
      return [_broadcast_to(arg, res_shape) for arg, shp in zip(args, shapes)]
    else:
      if all(len(shapes[0]) == len(s) for s in shapes[1:]):
        return args  # no need for rank promotion, so rely on lax promotion
      nonscalar_ranks = {len(shp) for shp in shapes if shp}
      if len(nonscalar_ranks) < 2:
        return args  # rely on lax scalar promotion
      else:
        if config.jax_numpy_rank_promotion != "allow":
          _rank_promotion_warning_or_error(fun_name, shapes)
        result_rank = len(lax.broadcast_shapes(*shapes))
        return [_broadcast_to(arg, (1,) * (result_rank - len(shp)) + shp)
                for arg, shp in zip(args, shapes)]
