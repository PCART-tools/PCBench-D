  def get_effect_type(self):
    return ErrorEffect(OOBError, (api.ShapeDtypeStruct((3,), jnp.int32),))
