@util._wraps(np.partition, lax_description="""
The JAX version requires the ``kth`` argument to be a static integer rather than
a general array. This is implemented via two calls to :func:`jax.lax.top_k`. If
you're only accessing the top or bottom k values of the output, it may be more
efficient to call :func:`jax.lax.top_k` directly.

The JAX version differs from the NumPy version in the treatment of NaN entries;
NaNs which have the negative bit set are sorted to the beginning of the array.
""")
@partial(jit, static_argnames=['kth', 'axis'])
def partition(a: ArrayLike, kth: int, axis: int = -1) -> Array:
  # TODO(jakevdp): handle NaN values like numpy.
  util._check_arraylike("partition", a)
  arr = asarray(a)
  if issubdtype(arr.dtype, np.complexfloating):
    raise NotImplementedError("jnp.partition for complex dtype is not implemented.")
  axis = _canonicalize_axis(axis, arr.ndim)
  kth = _canonicalize_axis(kth, arr.shape[axis])

  arr = swapaxes(arr, axis, -1)
  bottom = -lax.top_k(-arr, kth + 1)[0]
  top = lax.top_k(arr, arr.shape[-1] - kth - 1)[0]
  out = lax.concatenate([bottom, top], dimension=arr.ndim - 1)
  return swapaxes(out, -1, axis)
