def _householder_product_batching_rule(batched_args, batch_dims):
  a, taus = batched_args
  b_a, b_taus, = batch_dims
  return householder_product(batching.moveaxis(a, b_a, 0),
               batching.moveaxis(taus, b_taus, 0)), (0,)
