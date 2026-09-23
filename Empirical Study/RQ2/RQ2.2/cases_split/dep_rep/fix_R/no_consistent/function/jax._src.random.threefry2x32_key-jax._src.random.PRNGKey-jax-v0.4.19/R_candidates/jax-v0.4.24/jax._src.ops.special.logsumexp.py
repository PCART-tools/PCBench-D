def logsumexp(a: ArrayLike, axis: Axis = None, b: ArrayLike | None = None,
              keepdims: bool = False, return_sign: bool = False) -> Array | tuple[Array, Array]:
  r"""Log-sum-exp reduction.

  Computes

  .. math::
    \mathrm{logsumexp}(a) = \mathrm{log} \sum_j b \cdot \mathrm{exp}(a_{ij})

  where the :math:`j` indices range over one or more dimensions to be reduced.

  Args:
    a: the input array
    axis: the axis or axes over which to reduce. May be either ``None``, an
      int, or a tuple of ints.
    b: scaling factors for :math:`\mathrm{exp}(a)`. Must be broadcastable to the
      shape of `a`.
    keepdims: If ``True``, the axes that are reduced are left in the output as
      dimensions of size 1.
    return_sign: If ``True``, the output will be a ``(result, sign)`` pair,
      where ``sign`` is the sign of the sums and ``result`` contains the
      logarithms of their absolute values. If ``False`` only ``result`` is
      returned and it will contain NaN values if the sums are negative.

  Returns:
    Either an array ``result`` or a pair of arrays ``(result, sign)``, depending
    on the value of the ``return_sign`` argument.
  """
  if b is not None:
    a_arr, b_arr = promote_args_inexact("logsumexp", a, b)
    a_arr = jnp.where(b_arr != 0, a_arr, -jnp.inf)
  else:
    a_arr, = promote_args_inexact("logsumexp", a)
    b_arr = a_arr  # for type checking
  pos_dims, dims = _reduction_dims(a_arr, axis)
  amax = jnp.max(a_arr.real, axis=dims, keepdims=keepdims)
  amax = lax.stop_gradient(lax.select(jnp.isfinite(amax), amax, lax.full_like(amax, 0)))
  amax_with_dims = amax if keepdims else lax.expand_dims(amax, pos_dims)

  exp_a = lax.exp(lax.sub(a_arr, amax_with_dims.astype(a_arr.dtype)))
  if b is not None:
    exp_a = lax.mul(exp_a, b_arr)
  sumexp = exp_a.sum(axis=dims, keepdims=keepdims)
  sign = lax.sign(sumexp)
  if return_sign or not np.issubdtype(a_arr.dtype, np.complexfloating):
    sumexp = abs(sumexp)
  out = lax.add(lax.log(sumexp), amax.astype(sumexp.dtype))

  if return_sign:
    return (out, sign)
  if b is not None and not np.issubdtype(out.dtype, np.complexfloating):
    with jax.debug_nans(False):
      out = jnp.where(sign < 0, jnp.array(np.nan, dtype=out.dtype), out)
  return out
