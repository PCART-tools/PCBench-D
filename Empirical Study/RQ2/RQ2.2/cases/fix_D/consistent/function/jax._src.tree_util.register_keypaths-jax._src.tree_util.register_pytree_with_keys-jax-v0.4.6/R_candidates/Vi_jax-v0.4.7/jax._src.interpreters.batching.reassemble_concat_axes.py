def reassemble_concat_axes(vals, dims):
  idxs = {d.segment_lengths.val for d in dims if isinstance(d, ConcatAxis)}
  dims = [ConcatAxis(d.axis, vals[d.segment_lengths.val])
          if isinstance(d, ConcatAxis) else d for d in dims]
  vals = [x for i, x in enumerate(vals) if i not in idxs]
  return vals, dims
