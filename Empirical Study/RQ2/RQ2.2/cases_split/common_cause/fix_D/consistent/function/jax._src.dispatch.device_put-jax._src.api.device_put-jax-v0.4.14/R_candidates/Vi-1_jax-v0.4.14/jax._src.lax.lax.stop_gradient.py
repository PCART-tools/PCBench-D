def stop_gradient(x: T) -> T:
  """Stops gradient computation.

  Operationally ``stop_gradient`` is the identity function, that is, it returns
  argument `x` unchanged. However, ``stop_gradient`` prevents the flow of
  gradients during forward or reverse-mode automatic differentiation. If there
  are multiple nested gradient computations, ``stop_gradient`` stops gradients
  for all of them.

  For example:

  >>> jax.grad(lambda x: x**2)(3.)
  Array(6., dtype=float32, weak_type=True)
  >>> jax.grad(lambda x: jax.lax.stop_gradient(x)**2)(3.)
  Array(0., dtype=float32, weak_type=True)
  >>> jax.grad(jax.grad(lambda x: x**2))(3.)
  Array(2., dtype=float32, weak_type=True)
  >>> jax.grad(jax.grad(lambda x: jax.lax.stop_gradient(x)**2))(3.)
  Array(0., dtype=float32, weak_type=True)
  """
  def stop(x):
    # only bind primitive on inexact dtypes, to avoid some staging
    if dtypes.issubdtype(core.get_aval(x).dtype, dtypes.extended):
      return x
    elif (dtypes.issubdtype(_dtype(x), np.floating) or
        dtypes.issubdtype(_dtype(x), np.complexfloating)):
      return ad_util.stop_gradient_p.bind(x)
    else:
      return x
  return tree_map(stop, x)
