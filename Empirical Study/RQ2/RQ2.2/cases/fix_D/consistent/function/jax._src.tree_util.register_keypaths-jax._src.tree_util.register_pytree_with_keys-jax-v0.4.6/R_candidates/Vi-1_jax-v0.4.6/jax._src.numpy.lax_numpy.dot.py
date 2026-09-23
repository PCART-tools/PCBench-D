@util._wraps(np.dot, lax_description=_PRECISION_DOC)
@partial(jit, static_argnames=('precision',), inline=True)
def dot(a, b, *, precision=None):  # pylint: disable=missing-docstring
  util._check_arraylike("dot", a, b)
  a, b = util._promote_dtypes(a, b)
  a_ndim, b_ndim = ndim(a), ndim(b)
  if a_ndim == 0 or b_ndim == 0:
    return lax.mul(a, b)
  if _max(a_ndim, b_ndim) <= 2:
    return lax.dot(a, b, precision=precision)

  if b_ndim == 1:
    contract_dims = ((a_ndim - 1,), (0,))
  else:
    contract_dims = ((a_ndim - 1,), (b_ndim - 2,))
  batch_dims = ((), ())
  return lax.dot_general(a, b, (contract_dims, batch_dims), precision)
