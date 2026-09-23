def _make_unary_elementwise_harness(*, prim, shape=(20, 20), dtype):
  define(
      str(prim),
      f"shape={jtu.format_shape_dtype_string(shape, dtype)}",
      prim.bind, [RandArg(shape, dtype)],
      prim=prim,
      dtype=dtype,
      shape=shape)
