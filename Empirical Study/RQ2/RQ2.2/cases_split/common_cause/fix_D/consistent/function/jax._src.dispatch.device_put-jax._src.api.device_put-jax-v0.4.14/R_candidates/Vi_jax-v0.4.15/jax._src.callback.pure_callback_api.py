def pure_callback_api(
    callback: Callable[..., Any],
    result_shape_dtypes: Any,
    *args: Any,
    sharding: SingleDeviceSharding | None = None,
    vectorized: bool = False,
    **kwargs: Any,
):
  """Applies a functionally pure Python callable. Works under :func:`jit`/:func:`~pmap`/etc.

  ``pure_callback`` enables calling a Python function in JIT-ed JAX functions.
  The input ``callback`` will be passed NumPy arrays in place of JAX arrays and
  should also return NumPy arrays. Execution takes place on CPU, like any
  Python+NumPy function.

  The callback is treated as functionally pure, meaning it has no side-effects
  and its output value depends only on its argument values. As a consequence, it
  is safe to be called multiple times (e.g. when transformed by :func:`~vmap` or
  :func:`~pmap`), or not to be called at all when e.g. the output of a
  `jit`-decorated function has no data dependence on its value. Pure callbacks
  may also be reordered if data-dependence allows.

  When :func:`~pmap`-ed, the pure callback will be called several times (one on each
  axis of the map). When `vmap`-ed the behavior will depend on the value of the
  ``vectorized`` keyword argument. When ``vectorized`` is ``True``, the callback
  is assumed to obey
  ``jax.vmap(callback)(xs) == callback(xs) == jnp.stack([callback(x) for x in xs])``.
  Therefore, the callback will be called directly on batched inputs (where the
  batch axes are the leading dimensions). Additionally, the callbacks should
  return outputs that have corresponding leading batch axes. If not vectorized
  ``callback`` will be mapped sequentially across the batched axis.
  For example, if ``callback = lambda x, y: np.matmul(x, y)``, then we are free
  to set ``vectorized=True`` because the ``np.matmul`` function handles
  arbitrary leading batch dimensions.

  Args:
    callback: A Python callable. The callable will be passed PyTrees of NumPy
      arrays as arguments, and should return a PyTree of NumPy arrays that
      matches ``result_shape_dtypes``.
    result_shape_dtypes: A PyTree with leaves that are objects with ``shape``
      and ``dtype`` attributes which represent to the shapes and dtypes of the
      value of ``callback`` applied to ``args`` and ``kwargs``.
    *args: The positional arguments to the callback. Must be PyTrees of JAX
      types.
    sharding: optional sharding that specifies the device from which the
      callback should be invoked.
    vectorized: A boolean that indicates whether or not ``callback`` is
      vectorized, meaning it can handle arrays with additional leading
      dimensions. If ``vectorized`` is `True`, when the callback is mapped
      via `jax.vmap`, it will be called directly on inputs with leading batch
      dimensions instead of executing ``callback`` on each mapped input
      individually. The callback should also return outputs batched across the
      leading axis. By default, ``vectorized`` is ``False``.
    **kwargs: The keyword arguments to the callback. Must be PyTrees of JAX
      types.

  Returns:
    The value of ``callback(*args, **kwargs)``.
  """
  return pure_callback(
      callback,
      result_shape_dtypes,
      *args,
      sharding=sharding,
      vectorized=vectorized,
      **kwargs,
  )
