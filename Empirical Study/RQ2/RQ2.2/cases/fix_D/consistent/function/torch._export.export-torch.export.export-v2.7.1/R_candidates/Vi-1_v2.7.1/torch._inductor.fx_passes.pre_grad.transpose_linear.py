def transpose_linear(
    input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor]
) -> torch.Tensor:
    if bias is None:
        return torch.matmul(input.transpose(-1, -2), weight.t())
    return torch.matmul(input.transpose(-1, -2), weight.t()) + bias
