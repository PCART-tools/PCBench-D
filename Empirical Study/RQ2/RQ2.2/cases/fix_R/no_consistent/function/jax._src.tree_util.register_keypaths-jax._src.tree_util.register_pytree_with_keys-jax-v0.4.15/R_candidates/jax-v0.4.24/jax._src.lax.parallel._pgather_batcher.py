def _pgather_batcher(vals_in, dims_in, *, axes):
  src, idx = vals_in
  dsrc, didx = dims_in
  if didx is not batching.not_mapped and dsrc is not batching.not_mapped:
    # NB: We could just go forward with it and take the diagonal along the
    #     two axes we get in the output, but that would be quite inefficient
    raise NotImplementedError("Please open a feature request!")
  elif didx is not batching.not_mapped:
    return pgather_p.bind(src, idx, axes=axes), didx
  elif dsrc is not batching.not_mapped:
    src_last_batched = moveaxis(src, dsrc, -1)
    result = pgather_p.bind(src_last_batched, idx, axes=axes)
    return result, result.ndim - 1
  else:
    assert False  # This shouldn't get called anyway
