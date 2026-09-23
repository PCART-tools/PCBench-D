def _get_states(attrs_tracked):
  from jax.experimental.attrs import jax_getattr  # type: ignore
  return [jax_getattr(obj, attr) for (obj, attr) in attrs_tracked]
