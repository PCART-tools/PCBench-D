def device_put(x, device: Optional[xc.Device] = None):
  """Transfers ``x`` to ``device``.

  Args:
    x: An array, scalar, or (nested) standard Python container thereof.
    device: The (optional) :py:class:`Device` to which ``x`` should be
      transferred. If given, then the result is committed to the device.

  If the ``device`` parameter is ``None``, then this operation behaves like the
  identity function if the operand is on any device already, otherwise it
  transfers the data to the default device, uncommitted.

  For more details on data placement see the
  :ref:`FAQ on data placement <faq-data-placement>`.

  This function is always asynchronous, i.e. returns immediately.

  Returns:
    A copy of ``x`` that resides on ``device``.
  """
  with config_explicit_device_put_scope():
    return tree_map(lambda y: dispatch.device_put_p.bind(y, device=device), x)
