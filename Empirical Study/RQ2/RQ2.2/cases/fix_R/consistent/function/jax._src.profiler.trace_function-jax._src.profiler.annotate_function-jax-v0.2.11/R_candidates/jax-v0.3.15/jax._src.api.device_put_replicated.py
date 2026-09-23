def device_put_replicated(x: Any, devices: Sequence[xc.Device]):  # noqa: F811
  """Transfer array(s) to each specified device and form ShardedDeviceArray(s).

  Args:
    x: an array, scalar, or (nested) standard Python container thereof
      representing the array to be replicated to form the output.
    devices: A sequence of :py:class:`Device` instances representing the devices
      to which ``x`` will be transferred.

  This function is always asynchronous, i.e. returns immediately.

  Returns:
    A ShardedDeviceArray or (nested) Python container thereof representing the
    value of ``x`` broadcasted along a new leading axis of size
    ``len(devices)``, with each slice along that new leading axis backed by
    memory on the device specified by the corresponding entry in ``devices``.

  Examples:
    Passing an array:

    >>> import jax
    >>> devices = jax.local_devices()
    >>> x = jax.numpy.array([1., 2., 3.])
    >>> y = jax.device_put_replicated(x, devices)
    >>> np.allclose(y, jax.numpy.stack([x for _ in devices]))
    True

  See Also:
    - device_put
    - device_put_sharded
  """
  if not isinstance(devices, Sequence) or not devices:
    raise ValueError("`devices` argument to `device_put_replicated must be "
                     "a non-empty sequence.")
  def _device_put_replicated(x):
    aval = core.unmapped_aval(len(devices), core.no_axis_name, 0,
                              core.raise_to_shaped(core.get_aval(x)))
    assert (isinstance(aval, ShapedArray) and
            len(xla.aval_to_xla_shapes(aval)) == 1)
    buf, = dispatch.device_put(x, devices[0])
    rest_bufs = [buf.copy_to_device(d) for d in devices[1:]]
    if config.jax_array:
      from jax.experimental import array, sharding
      sharding_spec = pxla._create_pmap_sharding_spec(aval)
      return array.Array(
          aval.shape, sharding.PmapSharding(np.array(devices), sharding_spec),
          [buf, *rest_bufs], committed=True)
    else:
      return pxla.make_sharded_device_array(aval, None, [buf, *rest_bufs])

  with config_explicit_device_put_scope():
    return tree_map(_device_put_replicated, x)
