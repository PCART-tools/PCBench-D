@random_seed_p.def_impl
def random_seed_impl(seeds, *, impl):
  base_arr = random_seed_impl_base(seeds, impl=impl)
  return PRNGKeyArrayImpl(impl, base_arr)
