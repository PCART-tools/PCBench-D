@maybe_dequantize_first_two_tensor_args_and_handle_tuples
def compute_sqnr(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    Ps = torch.norm(x)
    Pn = torch.norm(x - y)
    return 20 * torch.log10(Ps / Pn)
