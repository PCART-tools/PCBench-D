def resolve_ragged_axes(vals, dims):
  idxs = {lengths_idx.val for d in dims if isinstance(d, RaggedAxis)
          for (_, lengths_idx) in d.ragged_axes}
  dims = [RaggedAxis(d.stacked_axis,
                     tuple([(ragged_axis, vals[lengths_idx.val])
                            for ragged_axis, lengths_idx in d.ragged_axes]))
          if isinstance(d, RaggedAxis) else d for d in dims]
  vals = [x for i, x in enumerate(vals) if i not in idxs]
  return vals, dims
