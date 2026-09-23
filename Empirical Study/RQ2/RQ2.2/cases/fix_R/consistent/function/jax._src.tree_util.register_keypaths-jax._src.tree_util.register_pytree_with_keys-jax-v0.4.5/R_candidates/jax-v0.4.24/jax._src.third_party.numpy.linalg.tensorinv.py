@implements(np.linalg.tensorinv)
def tensorinv(a, ind=2):
  check_arraylike('jnp.linalg.tensorinv', a)
  a = jnp.asarray(a)
  oldshape = a.shape
  prod = 1
  if ind > 0:
    invshape = oldshape[ind:] + oldshape[:ind]
    for k in oldshape[ind:]:
      prod *= k
  else:
    raise ValueError("Invalid ind argument.")
  a = a.reshape(prod, -1)
  ia = la.inv(a)
  return ia.reshape(*invshape)
