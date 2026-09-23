def trt_transposed_matmul(lhs: torch.Tensor, rhs: torch.Tensor, lhs_transposed: bool, rhs_transposed: bool):
    if lhs_transposed:
        lhs = lhs.transpose(-1, -2)
    if rhs_transposed:
        rhs = rhs.transpose(-1, -2)
    return torch.matmul(lhs, rhs)
