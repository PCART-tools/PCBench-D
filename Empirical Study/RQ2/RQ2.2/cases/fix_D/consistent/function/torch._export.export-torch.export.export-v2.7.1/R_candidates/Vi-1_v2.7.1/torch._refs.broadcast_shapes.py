def broadcast_shapes(*shapes) -> ShapeType:
    return torch.Size(_broadcast_shapes(*shapes))
