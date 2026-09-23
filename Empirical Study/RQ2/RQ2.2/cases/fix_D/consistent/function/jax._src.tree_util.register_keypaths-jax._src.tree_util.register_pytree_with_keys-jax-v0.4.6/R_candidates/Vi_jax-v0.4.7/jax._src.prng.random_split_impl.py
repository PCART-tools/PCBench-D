@random_split_p.def_impl
def random_split_impl(keys, *, count):
  base_arr = random_split_impl_base(
      keys.impl, keys.unsafe_raw_array(), keys.ndim, count=count)
  return PRNGKeyArray(keys.impl, base_arr)
