def psum_scatter(x, axis_name, *, scatter_dimension=0, axis_index_groups=None, tiled=False):
  """Compute an all-reduce sum over the axis ``axis_name``, and scatter the result.

  Args:
    x: array(s) with a mapped axis named ``axis_name``.
    axis_name: hashable Python object used to name a pmapped axis (see the
      :func:`jax.pmap` documentation for more details).
    scatter_dimension: a positional axis into which the all reduce result along
      ``axis_name`` will be scattered.
    axis_index_groups: optional list of lists containing axis indices (e.g. for
      an axis of size 4, [[0, 1], [2, 3]] would run reduce-scatter over the
      first two and the last two replicas). Groups must cover all axis indices
      exactly once, and all groups must be the same size.
    tiled: when ``False``, the size of dimension in ``scatter_dimension`` must
      match the size of axis ``axis_name`` (or the group size if
      ``axis_index_groups`` is given). After scattering the all reduce result
      along ``scatter_dimension``, the output is sequeezed by removing
      ``scatter_dimension``. When ``True``, the size of dimension in
      ``scatter_dimension` must be dividible by the size of axis ``axis_name``
      (or the group size if ``axis_index_groups`` is given),
      and ``scatter_dimension`` is preserved.

  Returns:
    Array(s) with the similar shape as ``x``, except the size of dimension in
    position``scatter_dimension`` is divided by the size of axis ``axis_name``.

  For example, with 4 XLA devices available:

  >>> x = np.arange(16).reshape(4, 4)
  >>> print(x)
  [[ 0  1  2  3]
   [ 4  5  6  7]
   [ 8  9 10 11]
   [12 13 14 15]]
  >>> y = jax.pmap(lambda x: jax.lax.psum_scatter(x, 'i'), axis_name='i')(x)
  >>> print(y)
  [24 28 32 36]

  if using tiled:

  >>> y = jax.pmap(lambda x: jax.lax.psum_scatter(x, 'i', tiled=True), axis_name='i')(x)
  >>> print(y)
  [[24]
   [28]
   [32]
   [36]]

  An example of using axis_index_groups:

  >>> def f(x):
  ...   return jax.lax.psum_scatter(
  ...       x, 'i', axis_index_groups=[[0, 2], [3, 1]], tiled=True)
  >>> y = jax.pmap(f, axis_name='i')(x)
  >>> print(y)
  [[ 8 10]
   [20 22]
   [12 14]
   [16 18]]
  """
  axis_size = psum(1, axis_name, axis_index_groups=axis_index_groups)
  axis_index_groups = _canonicalize_axis_index_groups(axis_index_groups)
  bind = partial(
      reduce_scatter_p.bind,
      axis_name=axis_name,
      scatter_dimension=scatter_dimension,
      axis_index_groups=axis_index_groups,
      axis_size=axis_size,
      tiled=tiled)
  return tree_util.tree_map(bind, x)
