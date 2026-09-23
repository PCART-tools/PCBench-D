def _no_grad_embedding_renorm_(weight: Tensor, input: Tensor, max_norm: float, norm_type: float) -> Tensor:
    with torch.no_grad():
        torch.embedding_renorm_(weight, input, max_norm, norm_type)
