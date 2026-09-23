@random_fold_in_p.def_impl
def random_fold_in_impl(keys, msgs):
  base_arr = random_fold_in_impl_base(
      keys.impl, keys.unsafe_raw_array(), msgs, keys.shape)
  return PRNGKeyArrayImpl(keys.impl, base_arr)
