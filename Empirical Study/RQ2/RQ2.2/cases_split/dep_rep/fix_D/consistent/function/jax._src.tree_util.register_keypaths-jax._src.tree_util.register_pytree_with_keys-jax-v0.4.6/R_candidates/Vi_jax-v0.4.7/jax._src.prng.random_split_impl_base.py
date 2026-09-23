def random_split_impl_base(impl, base_arr, keys_ndim, *, count):
  split = iterated_vmap_unary(keys_ndim, lambda k: impl.split(k, count))
  return split(base_arr)
