@api_boundary
def map(f, xs):
  """Map a function over leading array axes.

  Like Python's builtin map, except inputs and outputs are in the form of
  stacked arrays. Consider using the ``jax.vmap`` transform instead, unless you
  need to apply a function element by element for reduced memory usage or
  heterogeneous computation with other control flow primitives.

  When ``xs`` is an array type, the semantics of ``map`` are given by this
  Python implementation::

    def map(f, xs):
      return np.stack([f(x) for x in xs])

  Like ``scan``, ``map`` is implemented in terms of JAX primitives so many of
  the same advantages over a Python loop apply: ``xs`` may be an arbitrary
  nested pytree type, and the mapped computation is compiled only once.

  Args:
    f: a Python function to apply element-wise over the first axis or axes of
      ``xs``.
    xs: values over which to map along the leading axis.

  Returns:
    Mapped values.
  """
  g = lambda _, x: ((), f(x))
  _, ys = scan(g, (), xs)
  return ys
