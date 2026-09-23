def _sparse_to_dense(tensor):
    if tensor.dtype != torch.bool:
        return tensor.to_dense()

    # to_dense uses coalesce which isn't implemented for bool
    return tensor.to(torch.int8).to_dense().to(torch.bool)
