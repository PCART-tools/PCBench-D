def broadcast_batcher(prim, args, dims, **params):
  """Process a primitive with built-in broadcasting.

  Args:
    args: the possibly-batched arguments
    dims: list or tuple of the same length as `args`, where each
      entry indicates the batching state of the corresponding entry to `args`:
      either an int indicating the batch dimension, or else `not_mapped`
      indicating no batching.
  """
  assert len(args) > 1
  shape, dim = next((x.shape, d) for x, d in zip(args, dims)
                    if d is not not_mapped)
  if all(core.symbolic_equal_shape(shape, x.shape) and d == dim
         for x, d in zip(args, dims) if np.ndim(x)):
    # if there's only agreeing batch dims and scalars, just call the primitive
    out = prim.bind(*args, **params)
    return (out, (dim,) * len(out)) if prim.multiple_results else (out, dim)
  else:
    # We pass size of 1 here because (1) at least one argument has a real batch
    # dimension and (2) all unmapped axes can have a singleton axis inserted and
    # then rely on the primitive's built-in broadcasting.
    args = [bdim_at_front(x, d, 1) if np.ndim(x) else x
            for x, d in zip(args, dims)]
    ndim = max(np.ndim(x) for x in args)  # special-case scalar broadcasting
    args = [_handle_scalar_broadcasting(ndim, x, d) for x, d in zip(args, dims)]
    out = prim.bind(*args, **params)
    return (out, (0,) * len(out)) if prim.multiple_results else (out, 0)
