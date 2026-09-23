class Precision(xla_client.PrecisionConfig.Precision):  # type: ignore
  """Precision enum for lax functions

  The `precision` argument to JAX functions generally controls the tradeoff
  between speed and accuracy for array computations on accelerator backends,
  (i.e. TPU and GPU). Members are:

  DEFAULT:
    Fastest mode, but least accurate. Performs computations in bfloat16.
    Aliases: ``'default'``, ``'fastest'``, ``'bfloat16'``.
  HIGH:
    Slower but more accurate. Performs float32 computations in 3 bfloat16
    passes, or using tensorfloat32 where available. Aliases: ``'high'``,
    ``'bfloat16_3x'``, ``'tensorfloat32'``.
  HIGHEST:
    Slowest but most accurate. Performs computations in float32 or float64
    as applicable. Aliases: ``'highest'``, ``'float32'``.
  """
  # Wrap enum values with this class.
  DEFAULT = _enum_descriptor('default')
  HIGH = _enum_descriptor('high')
  HIGHEST = _enum_descriptor('highest')

  _strings = {
      'highest':       xla_client.PrecisionConfig.Precision.HIGHEST,
      'float32':       xla_client.PrecisionConfig.Precision.HIGHEST,
      'high':          xla_client.PrecisionConfig.Precision.HIGH,
      'bfloat16_3x':   xla_client.PrecisionConfig.Precision.HIGH,
      'tensorfloat32': xla_client.PrecisionConfig.Precision.HIGH,
      'default':       xla_client.PrecisionConfig.Precision.DEFAULT,
      'bfloat16':      xla_client.PrecisionConfig.Precision.DEFAULT,
      'fastest':       xla_client.PrecisionConfig.Precision.DEFAULT,
      None:            xla_client.PrecisionConfig.Precision.DEFAULT,
  }
  def __init__(self, arg0):
    arg0 = self._strings.get(arg0, arg0)
    super().__init__(arg0)

  def __str__(self) -> str:
    return self.name
