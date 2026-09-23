def _schur_batching_rule(batched_args, batch_dims, *, compute_schur_vectors,
                         sort_eig_vals, select_callable):
  x, = batched_args
  bd, = batch_dims
  x = batching.moveaxis(x, bd, 0)

  return schur_p.bind(
      x,
      compute_schur_vectors=compute_schur_vectors,
      sort_eig_vals=sort_eig_vals,
      select_callable=select_callable), (0,) * (1 + compute_schur_vectors)
