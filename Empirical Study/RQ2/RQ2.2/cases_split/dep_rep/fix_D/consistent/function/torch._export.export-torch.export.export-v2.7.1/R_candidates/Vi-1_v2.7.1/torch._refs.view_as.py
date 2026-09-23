def view_as(self: TensorLikeType, other: TensorLikeType) -> TensorLikeType:
    return self.view(other.size())
