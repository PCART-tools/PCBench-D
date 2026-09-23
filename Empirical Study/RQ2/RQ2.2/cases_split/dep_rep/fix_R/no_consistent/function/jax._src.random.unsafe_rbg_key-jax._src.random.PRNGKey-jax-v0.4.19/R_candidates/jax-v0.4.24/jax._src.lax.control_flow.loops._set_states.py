def _set_states(attrs_tracked, vals):
  from jax.experimental.attrs import jax_setattr  # type: ignore
  for ((obj, attr), val) in zip(attrs_tracked, vals):
    jax_setattr(obj, attr, val)
