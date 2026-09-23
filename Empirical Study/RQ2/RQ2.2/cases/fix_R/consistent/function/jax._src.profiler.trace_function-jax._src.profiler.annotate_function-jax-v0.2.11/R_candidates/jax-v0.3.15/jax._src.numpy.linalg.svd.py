@_wraps(np.linalg.svd)
@partial(jit, static_argnames=('full_matrices', 'compute_uv', 'hermitian'))
def svd(a, full_matrices: bool = True, compute_uv: bool = True,
        hermitian: bool = False):
  a, = _promote_dtypes_inexact(jnp.asarray(a))
  if hermitian:
    w, v = lax_linalg.eigh(a)
    s = lax.abs(v)
    if compute_uv:
      sign = lax.sign(v)
      idxs = lax.broadcasted_iota(np.int64, s.shape, dimension=s.ndim - 1)
      s, idxs, sign = lax.sort((s, idxs, sign), dimension=-1, num_keys=1)
      s = lax.rev(s, dimensions=[s.ndim - 1])
      idxs = lax.rev(idxs, dimensions=[s.ndim - 1])
      sign = lax.rev(sign, dimensions=[s.ndim - 1])
      u = jnp.take_along_axis(w, idxs[..., None, :], axis=-1)
      vh = _H(u * sign[..., None, :].astype(u.dtype))
      return u, s, vh
    else:
      return lax.rev(lax.sort(s, dimension=-1), dimensions=[s.ndim-1])

  return lax_linalg.svd(a, full_matrices=full_matrices, compute_uv=compute_uv)
