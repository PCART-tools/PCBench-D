  def __hash__(self):
    # TODO(frostig): avoid the conversion from dict by addressing
    # https://github.com/google/jax/issues/8182
    named = frozenset(self.named_shape.items())
    return hash((self.shape, self.dtype, named, self.sharding, self.layout))
