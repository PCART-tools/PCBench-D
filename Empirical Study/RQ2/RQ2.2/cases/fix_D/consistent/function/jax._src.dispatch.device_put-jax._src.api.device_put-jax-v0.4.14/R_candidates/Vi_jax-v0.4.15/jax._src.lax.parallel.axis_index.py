def axis_index(axis_name):
  """Return the index along the mapped axis ``axis_name``.

  Args:
    axis_name: hashable Python object used to name the mapped axis.

  Returns:
    An integer representing the index.

  For example, with 8 XLA devices available:

  >>> from functools import partial
  >>> @partial(jax.pmap, axis_name='i')
  ... def f(_):
  ...   return lax.axis_index('i')
  ...
  >>> f(np.zeros(4))
  Array([0, 1, 2, 3], dtype=int32)
  >>> f(np.zeros(8))
  Array([0, 1, 2, 3, 4, 5, 6, 7], dtype=int32)
  >>> @partial(jax.pmap, axis_name='i')
  ... @partial(jax.pmap, axis_name='j')
  ... def f(_):
  ...   return lax.axis_index('i'), lax.axis_index('j')
  ...
  >>> x, y = f(np.zeros((4, 2)))
  >>> print(x)
  [[0 0]
  [1 1]
  [2 2]
  [3 3]]
  >>> print(y)
  [[0 1]
  [0 1]
  [0 1]
  [0 1]]
  """
  return axis_index_p.bind(axis_name=axis_name)
