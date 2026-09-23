def _eye_like_xla(c, aval):
  iota_shape = xla_client.Shape.array_shape(
      xla.dtype_to_primitive_type(np.dtype(np.int32)), aval.shape)
  x = xops.Eq(xops.Iota(c, iota_shape, len(aval.shape) - 1),
              xops.Iota(c, iota_shape, len(aval.shape) - 2))
  return xops.ConvertElementType(x, xla.dtype_to_primitive_type(aval.dtype))
