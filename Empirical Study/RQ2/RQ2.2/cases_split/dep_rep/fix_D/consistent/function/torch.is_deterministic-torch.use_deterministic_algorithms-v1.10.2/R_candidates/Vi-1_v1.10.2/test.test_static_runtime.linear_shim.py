def linear_shim(
    input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor] = None
) -> torch.Tensor:
    output = input.matmul(weight.t())
    if bias is not None:
        output += bias
    ret = output
    return ret
