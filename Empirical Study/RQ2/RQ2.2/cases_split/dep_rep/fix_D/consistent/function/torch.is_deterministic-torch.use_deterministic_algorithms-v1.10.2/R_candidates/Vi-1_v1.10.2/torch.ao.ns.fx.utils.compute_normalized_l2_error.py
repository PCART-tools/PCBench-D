@maybe_dequantize_first_two_tensor_args_and_handle_tuples
def compute_normalized_l2_error(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    return torch.sqrt(((x - y) ** 2).sum() / (x ** 2).sum())
