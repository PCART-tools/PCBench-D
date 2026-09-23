def get(identifier):
  """Get a loss scale object."""
  if isinstance(identifier, six.integer_types + (float,)):
    return FixedLossScale(identifier)
  if identifier == 'dynamic':
    return DynamicLossScale()
  if isinstance(identifier, LossScale):
    return identifier
  elif identifier is None:
    return None
  else:
    raise ValueError('Could not interpret loss scale identifier: %s' %
                     identifier)
