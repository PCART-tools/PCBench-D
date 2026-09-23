def _concatenate_transpose_rule(t, *operands, dimension):
  operand_shapes = [o.aval.shape if ad.is_undefined_primal(o) else o.shape
                    for o in operands]
  if type(t) is ad_util.Zero:
    return [ad_util.Zero(o.aval) if ad.is_undefined_primal(o) else None
            for o in operands]
  else:
    limit_points = np.cumsum(
        [shape[dimension] for shape in operand_shapes]).tolist()
    starts = np.zeros((len(operands), t.ndim), dtype=int).tolist()
    limits = np.tile(t.shape, (len(operands), 1)).tolist()

    for i, s in enumerate(starts[1:]):
      s[dimension] = limit_points[:-1][i]
    for i, l in enumerate(limits):
      l[dimension] = limit_points[i]

    return [slicing.slice(t, start, limit) if ad.is_undefined_primal(o)
            else None for o, start, limit in zip(operands, starts, limits)]
