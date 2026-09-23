  def tree_flatten(self):
    return ([self._payload], (self.traceback_info, self.prim, self.operand_shape))
