def device_put(
    x, device: Union[None, xc.Device, jax.sharding.Sharding, Any] = None):
  """Transfers ``x`` to ``device``.

  Args:
    x: An array, scalar, or (nested) standard Python container thereof.
    device: The (optional) :py:class:`Device`, `Sharding`, or a (nested)
      `Sharding` in standard Python container (must be a tree prefix of ``x``),
      representing the device(s) to which ``x`` should be transferred. If
      given, then the result is committed to the device(s).

  Returns:
    A copy of ``x`` that resides on ``device``.

  If the ``device`` parameter is ``None``, then this operation behaves like the
  identity function if the operand is on any device already, otherwise it
  transfers the data to the default device, uncommitted.

  For more details on data placement see the
  :ref:`FAQ on data placement <faq-data-placement>`.

  This function is always asynchronous, i.e. returns immediately without
  blocking the calling Python thread until any transfers are completed.
  """
  with config_explicit_device_put_scope():
    if device is None or isinstance(device, (xc.Device, jax.sharding.Sharding)):
      return tree_map(lambda y: dispatch.device_put_p.bind(y, device=device), x)

    x_flat, treedef = tree_flatten(x)
    device_flat = flatten_axes("device_put device", treedef, device)
    out_flat = [
        dispatch.device_put_p.bind(y, device=d)
        for y, d in zip(x_flat, device_flat)
    ]
    return tree_unflatten(treedef, out_flat)
