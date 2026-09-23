  def __str__(self):
    return (f'out-of-bounds indexing for array of '
            f'shape {self.operand_shape}: '
            f'index {self._payload[0]} is out of bounds for axis '
            f'{self._payload[1]} with size {self._payload[2]}. ')
