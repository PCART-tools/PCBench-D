class OOBError(JaxException):

  def __init__(self, traceback_info, primitive_name, operand_shape, payload):
    super().__init__(traceback_info)
    self.prim = primitive_name
    self.operand_shape = operand_shape
    self._payload = payload

  def tree_flatten(self):
    return ([self._payload], (self.traceback_info, self.prim, self.operand_shape))

  @classmethod
  def tree_unflatten(cls, metadata, payload):
    return cls(*metadata, payload[0])

  def __str__(self):
    return (f'out-of-bounds indexing for array of '
            f'shape {self.operand_shape}: '
            f'index {self._payload[0]} is out of bounds for axis '
            f'{self._payload[1]} with size {self._payload[2]}. ')

  def get_effect_type(self):
    return ErrorEffect(OOBError, (api.ShapeDtypeStruct((3,), jnp.int32),))
