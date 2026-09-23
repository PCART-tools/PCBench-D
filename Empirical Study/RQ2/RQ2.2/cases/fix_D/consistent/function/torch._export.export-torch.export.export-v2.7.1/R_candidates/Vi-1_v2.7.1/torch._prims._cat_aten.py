def _cat_aten(tensors: Union[tuple[Tensor, ...], list[Tensor]], dim: int) -> Tensor:
    return torch.cat(tensors, dim)
