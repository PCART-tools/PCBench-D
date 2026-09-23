@random_split_p.def_impl
def random_split_impl(keys, *, shape):
  base_arr = random_split_impl_base(
      keys.impl, keys.unsafe_raw_array(), keys.ndim, shape=shape)
  return PRNGKeyArrayImpl(keys.impl, base_arr)
