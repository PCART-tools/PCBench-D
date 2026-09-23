def _is_from_gda(x):
  # It's occasionally possible to end up with two FROM_GDA singletons (e.g. if
  # pickling in_axis_resources and sending to other processes). Make sure this
  # doesn't cause an error to avoid user confusion.
  return isinstance(x, type(FROM_GDA))
