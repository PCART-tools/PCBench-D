@util.implements(np.argpartition, lax_description="""
The JAX version requires the ``kth`` argument to be a static integer rather than
a general array. This is implemented via two calls to :func:`jax.lax.top_k`. If
you're only accessing the top or bottom k values of the output, it may be more
efficient to call :func:`jax.lax.top_k` directly.

The JAX version differs from the NumPy version in the treatment of NaN entries;
NaNs which have the negative bit set are sorted to the beginning of the array.
""")
@partial(jit, static_argnames=['kth', 'axis'])
def argpartition(a: ArrayLike, kth: int, axis: int = -1) -> Array:
  # TODO(jakevdp): handle NaN values like numpy.
  util.check_arraylike("partition", a)
  arr = asarray(a)
  if issubdtype(arr.dtype, np.complexfloating):
    raise NotImplementedError("jnp.argpartition for complex dtype is not implemented.")
  axis = _canonicalize_axis(axis, arr.ndim)
  kth = _canonicalize_axis(kth, arr.shape[axis])

  arr = swapaxes(arr, axis, -1)
  bottom_ind = lax.top_k(-arr, kth + 1)[1]

  # To avoid issues with duplicate values, we compute the top indices via a proxy
  set_to_zero = lambda a, i: a.at[i].set(0)
  for _ in range(arr.ndim - 1):
    set_to_zero = jax.vmap(set_to_zero)
  proxy = set_to_zero(ones(arr.shape), bottom_ind)
  top_ind = lax.top_k(proxy, arr.shape[-1] - kth - 1)[1]
  out = lax.concatenate([bottom_ind, top_ind], dimension=arr.ndim - 1)
  return swapaxes(out, -1, axis)
