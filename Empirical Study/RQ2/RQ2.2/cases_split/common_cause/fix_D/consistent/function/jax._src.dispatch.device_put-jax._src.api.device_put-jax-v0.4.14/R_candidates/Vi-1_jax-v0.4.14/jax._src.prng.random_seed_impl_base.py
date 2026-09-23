def random_seed_impl_base(seeds, *, impl):
  seed = iterated_vmap_unary(seeds.ndim, impl.seed)
  return seed(seeds)
