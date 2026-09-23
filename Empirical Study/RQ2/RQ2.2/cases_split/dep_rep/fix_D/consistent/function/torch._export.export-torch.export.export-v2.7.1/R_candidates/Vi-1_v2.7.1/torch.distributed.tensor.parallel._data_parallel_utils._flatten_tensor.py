def _flatten_tensor(
    tensor: torch.Tensor,
) -> tuple[torch.Tensor, Optional[DTensorSpec]]:
    if isinstance(tensor, DTensor):
        tensor._local_tensor.requires_grad_()
        return tensor._local_tensor, tensor._spec
    return tensor, None
