def reshape_as(self: TensorLikeType, other: TensorLikeType) -> TensorLikeType:
    return self.reshape(other.size())
