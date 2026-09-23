@util.implements(np.kron)
@jit
def kron(a: ArrayLike, b: ArrayLike) -> Array:
  # TODO(jakevdp): Non-array input deprecated 2023-09-22; change to error.
  util.check_arraylike("kron", a, b, emit_warning=True)
  a, b = util.promote_dtypes(a, b)
  if ndim(a) < ndim(b):
    a = expand_dims(a, range(ndim(b) - ndim(a)))
  elif ndim(b) < ndim(a):
    b = expand_dims(b, range(ndim(a) - ndim(b)))
  a_reshaped = expand_dims(a, range(1, 2 * ndim(a), 2))
  b_reshaped = expand_dims(b, range(0, 2 * ndim(b), 2))
  out_shape = tuple(np.multiply(shape(a), shape(b)))
  return reshape(lax.mul(a_reshaped, b_reshaped), out_shape)
