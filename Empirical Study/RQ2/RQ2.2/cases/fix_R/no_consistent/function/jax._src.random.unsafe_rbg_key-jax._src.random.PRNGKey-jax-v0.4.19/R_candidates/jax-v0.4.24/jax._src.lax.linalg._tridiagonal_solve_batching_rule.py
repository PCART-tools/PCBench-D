def _tridiagonal_solve_batching_rule(
    batched_args, batch_dims, *, m, n, ldb, t):
  del m, n, ldb, t
  dl, d, du, b = batched_args
  bdl, bd, bdu, bb = batch_dims
  if (bdl is batching.not_mapped and
      bd is batching.not_mapped and
      bdu is batching.not_mapped):

    b = batching.moveaxis(b, bb, -2)
    b_flat = b.reshape(b.shape[:-3]  + (b.shape[-3], b.shape[-2] * b.shape[-1]))
    bdim_out = b.ndim - 2
    out_flat = tridiagonal_solve(dl, d, du, b_flat)
    return out_flat.reshape(b.shape), bdim_out
  else:
    size = next(t.shape[i] for t, i in zip(batched_args, batch_dims)
                if i is not None)
    dl = batching.bdim_at_front(dl, bdl, size)
    d = batching.bdim_at_front(d, bd, size)
    du = batching.bdim_at_front(du, bdu, size)
    b = batching.bdim_at_front(b, bb, size)
    return tridiagonal_solve(dl, d, du, b), 0
