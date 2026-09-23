@_wraps(getattr(np, "from_dlpack", None))
def from_dlpack(x):
  from jax.dlpack import from_dlpack  # pylint: disable=g-import-not-at-top
  return from_dlpack(x.__dlpack__())
