@device_id_p.def_abstract_eval
def _device_id_abstract_eval():
  return jax_core.ShapedArray((), jnp.dtype("int32"))
