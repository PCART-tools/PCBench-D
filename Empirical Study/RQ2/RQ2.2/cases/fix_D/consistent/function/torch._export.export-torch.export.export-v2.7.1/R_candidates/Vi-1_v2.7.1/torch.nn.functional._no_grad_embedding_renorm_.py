def _no_grad_embedding_renorm_(
    weight: Tensor,
    input: Tensor,
    max_norm: float,
    norm_type: float,
) -> tuple[Tensor, Tensor]:
    torch.embedding_renorm_(weight.detach(), input, max_norm, norm_type)
