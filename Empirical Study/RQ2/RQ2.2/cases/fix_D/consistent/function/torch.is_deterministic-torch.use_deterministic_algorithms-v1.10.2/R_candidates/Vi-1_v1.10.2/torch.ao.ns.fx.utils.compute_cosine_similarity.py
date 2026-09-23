@maybe_dequantize_first_two_tensor_args_and_handle_tuples
def compute_cosine_similarity(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    # For convolutions, the shape of the quantized weight has one additional
    # dimension compared to the shape of the fp32 weight. Match the shapes
    # to enable cosine similarity comparison.
    x = x.reshape(1, -1)
    y = y.reshape(1, -1)
    return torch.nn.functional.cosine_similarity(x, y)
