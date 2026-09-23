def running_under_ipython():
  """Returns true if we appear to be in an IPython session."""
  try:
    get_ipython()  # type: ignore
    return True
  except NameError:
    return False
