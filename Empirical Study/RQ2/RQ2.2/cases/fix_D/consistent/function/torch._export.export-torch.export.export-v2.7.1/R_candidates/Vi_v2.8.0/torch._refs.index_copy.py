@out_wrapper()
def index_copy(x: TensorLike, dim: int, index: TensorLike, tensor: TensorLike):
    return x.clone(memory_format=torch.contiguous_format).index_copy_(
        dim, index, tensor
    )
