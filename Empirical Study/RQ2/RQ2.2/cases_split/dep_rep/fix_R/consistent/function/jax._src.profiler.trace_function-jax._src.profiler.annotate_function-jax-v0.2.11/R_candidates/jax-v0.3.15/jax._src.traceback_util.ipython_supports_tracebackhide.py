def ipython_supports_tracebackhide():
  """Returns true if the IPython version supports __tracebackhide__."""
  import IPython  # type: ignore
  return IPython.version_info[:2] >= (7, 17)
