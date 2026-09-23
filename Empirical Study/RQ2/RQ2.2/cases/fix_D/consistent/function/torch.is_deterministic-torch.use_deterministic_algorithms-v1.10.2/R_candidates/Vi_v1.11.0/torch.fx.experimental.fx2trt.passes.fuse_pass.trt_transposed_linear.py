def trt_transposed_linear(input: torch.Tensor, weight: torch.Tensor, bias: torch.Tensor):
    return torch.matmul(input.transpose(-1, -2), weight.t()) + bias
