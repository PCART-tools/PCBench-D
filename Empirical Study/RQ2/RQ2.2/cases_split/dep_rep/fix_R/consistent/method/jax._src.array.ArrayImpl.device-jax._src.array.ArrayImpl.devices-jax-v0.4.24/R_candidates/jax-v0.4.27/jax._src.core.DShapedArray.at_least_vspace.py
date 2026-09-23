  def at_least_vspace(self):
    return DShapedArray(self.shape, primal_dtype_to_tangent_dtype(self.dtype),
                        self.weak_type)
