def _make_tensor_from_meta(
    example: Union[torch.Tensor, FakeTensor],
    device: torch.device,
) -> torch.Tensor:
    """
    Create a real tensor from a tensor.
    """
    return torch.empty(
        example.size(),
        dtype=example.dtype,
        layout=example.layout,
        device=device,
    )
