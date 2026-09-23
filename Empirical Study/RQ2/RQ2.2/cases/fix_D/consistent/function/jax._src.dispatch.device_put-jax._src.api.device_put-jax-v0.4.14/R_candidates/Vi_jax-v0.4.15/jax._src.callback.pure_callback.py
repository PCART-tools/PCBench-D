def pure_callback(
    callback: Callable[..., Any],
    result_shape_dtypes: Any,
    *args: Any,
    sharding: SingleDeviceSharding | None = None,
    vectorized: bool = False,
    **kwargs: Any,
):
  """Calls a pure Python callback.

  For more explanation, see `External Callbacks`_.

  Args:
    callback: function to execute on the host. The callback is assumed to be a pure
      function (i.e. one without side-effects): if an impure function is passed, it
      may behave in unexpected ways, particularly under transformation.
    result_shape_dtypes: pytree whose leaves have ``shape`` and ``dtype`` attributes,
      whose structure matches the expected output of the callback function at runtime.
    *args: arguments to be passed to the callback function
    sharding: optional sharding that specifies the device from which the callback should
      be invoked.
    vectorized: boolean specifying whether the callback function can operate in a
      vectorized manner.
    **kwargs: keyword arguments to be passed to the callback function

  Returns:
    result: a pytree of :class:`jax.Array` objects whose structure matches that of
      ``result_shape_dtypes``.

  See Also:
    - :func:`jax.experimental.io_callback`: callback designed for impure functions.
    - :func:`jax.debug.callback`: callback designed for general-purpose debugging.
    - :func:`jax.debug.print`: callback designed for printing.

  .. _External Callbacks: https://jax.readthedocs.io/en/latest/notebooks/external_callbacks.html
  """
  def _flat_callback(*flat_args):
    args, kwargs = tree_util.tree_unflatten(in_tree, flat_args)
    return tree_util.tree_leaves(callback(*args, **kwargs))

  flat_args, in_tree = tree_util.tree_flatten((args, kwargs))
  tree_util.tree_map(_check_shape_dtype, result_shape_dtypes)
  result_avals = tree_util.tree_map(
      lambda x: core.ShapedArray(x.shape, x.dtype), result_shape_dtypes)
  flat_result_avals, out_tree = tree_util.tree_flatten(result_avals)
  out_flat = pure_callback_p.bind(
      *flat_args,
      callback=_flat_callback,
      result_avals=tuple(flat_result_avals),
      sharding=sharding,
      vectorized=vectorized,
  )
  return tree_util.tree_unflatten(out_tree, out_flat)
