@_wraps(np.linalg.tensorsolve)
def tensorsolve(a, b, axes=None):
  check_arraylike('jnp.linalg.tensorsolve', a, b)
  a = jnp.asarray(a)
  b = jnp.asarray(b)
  an = a.ndim
  if axes is not None:
    allaxes = list(range(0, an))
    for k in axes:
      allaxes.remove(k)
      allaxes.insert(an, k)

    a = a.transpose(allaxes)

  Q = a.shape[-(an - b.ndim):]

  prod = 1
  for k in Q:
    prod *= k

  a = a.reshape(-1, prod)
  b = b.ravel()

  res = jnp.asarray(la.solve(a, b))
  res = res.reshape(Q)

  return res
