  def __init__(self, traceback_info, primitive_name, operand_shape, payload):
    super().__init__(traceback_info)
    self.prim = primitive_name
    self.operand_shape = operand_shape
    self._payload = payload
