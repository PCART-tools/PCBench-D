@compatibility(is_backward_compatible=False)
def serialize_shape(shape: torch.Size) -> str:
    return str(list(shape))
