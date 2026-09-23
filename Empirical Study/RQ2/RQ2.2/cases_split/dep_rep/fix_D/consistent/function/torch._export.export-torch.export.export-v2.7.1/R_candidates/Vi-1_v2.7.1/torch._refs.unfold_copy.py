@register_decomposition(aten.unfold_copy)
@out_wrapper()
def unfold_copy(self: TensorLikeType, dimension: int, size: int, step: int):
    return self.unfold(dimension, size, step).clone(
        memory_format=torch.contiguous_format
    )
