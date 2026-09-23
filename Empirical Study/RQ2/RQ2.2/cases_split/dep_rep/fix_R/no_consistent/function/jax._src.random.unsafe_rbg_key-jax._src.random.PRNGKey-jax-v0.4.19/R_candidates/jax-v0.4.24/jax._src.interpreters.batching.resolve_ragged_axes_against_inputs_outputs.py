def resolve_ragged_axes_against_inputs_outputs(in_vals, out_vals, dims):
  def fetch(idx):
    if isinstance(idx, pe.InDBIdx):
      return in_vals[idx.val]
    else:
      assert isinstance(idx, pe.OutDBIdx)
      return out_vals[idx.val]

  dims = [RaggedAxis(d.stacked_axis,
                     tuple((ragged_axis, fetch(lengths_idx))
                           for ragged_axis, lengths_idx in d.ragged_axes))
          if isinstance(d, RaggedAxis) else d for d in dims]
  return dims
