@compatibility(is_backward_compatible=False)
def serialize_stride(stride: Tuple[int]) -> str:
    return str(list(stride))
