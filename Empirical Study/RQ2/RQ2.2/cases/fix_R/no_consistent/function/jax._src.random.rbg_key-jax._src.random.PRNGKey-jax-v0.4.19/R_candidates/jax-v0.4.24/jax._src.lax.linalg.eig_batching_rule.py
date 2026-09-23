def eig_batching_rule(batched_args, batch_dims, *, compute_left_eigenvectors,
                      compute_right_eigenvectors):
  x, = batched_args
  bd, = batch_dims
  x = batching.moveaxis(x, bd, 0)

  return (eig_p.bind(x, compute_left_eigenvectors=compute_left_eigenvectors,
                     compute_right_eigenvectors=compute_right_eigenvectors),
          (0,) * (1 + compute_left_eigenvectors + compute_right_eigenvectors))
