  @classmethod
  def tree_unflatten(cls, aux_data, children) -> Slice:
    start, size = [
        a if a is not None else b for a, b in zip(children, aux_data[:2])
    ]
    return cls(start, size, aux_data[2])
