@random_wrap_p.def_impl
def random_wrap_impl(base_arr, *, impl):
  return PRNGKeyArrayImpl(impl, base_arr)
