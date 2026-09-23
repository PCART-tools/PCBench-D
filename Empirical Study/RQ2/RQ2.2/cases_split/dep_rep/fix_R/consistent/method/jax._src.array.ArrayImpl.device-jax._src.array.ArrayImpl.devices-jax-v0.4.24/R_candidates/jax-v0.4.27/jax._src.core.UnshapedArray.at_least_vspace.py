  def at_least_vspace(self) -> AbstractValue:
    return UnshapedArray(primal_dtype_to_tangent_dtype(self.dtype),
                         self.weak_type)
