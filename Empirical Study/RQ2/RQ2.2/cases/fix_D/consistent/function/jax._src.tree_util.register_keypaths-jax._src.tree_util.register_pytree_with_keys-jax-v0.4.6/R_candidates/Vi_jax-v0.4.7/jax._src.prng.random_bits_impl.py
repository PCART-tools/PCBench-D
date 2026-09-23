@random_bits_p.def_impl
def random_bits_impl(keys, *, bit_width, shape):
  return random_bits_impl_base(keys.impl, keys.unsafe_raw_array(), keys.ndim,
                               bit_width=bit_width, shape=shape)
