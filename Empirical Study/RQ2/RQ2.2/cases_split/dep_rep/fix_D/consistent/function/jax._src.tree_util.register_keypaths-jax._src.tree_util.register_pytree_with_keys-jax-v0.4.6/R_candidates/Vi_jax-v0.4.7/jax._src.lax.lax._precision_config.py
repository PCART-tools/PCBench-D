def _precision_config(precision):
  if precision is not None:
    config = xla_client.PrecisionConfig()
    if isinstance(precision, tuple):
      config.operand_precision.extend(precision)
    else:
      config.operand_precision.extend((precision, precision))
    return config
  return None
