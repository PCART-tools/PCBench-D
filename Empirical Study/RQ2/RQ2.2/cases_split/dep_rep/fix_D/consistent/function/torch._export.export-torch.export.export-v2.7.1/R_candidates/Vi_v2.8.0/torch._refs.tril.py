@register_decomposition(aten.tril)
@out_wrapper()
def tril(a: TensorLikeType, diagonal: int = 0) -> TensorLikeType:
    torch._check(
        a.ndim >= 2, lambda: "tril: input tensor must have at least 2 dimensions"
    )
    h, w = a.shape[-2:]
    mask = (
        torch.arange(w, device=a.device).unsqueeze(-2)
        - torch.arange(h, device=a.device).unsqueeze(-1)
    ) <= diagonal

    # aten.tril always returns a new contiguous tensor
    # contiguous() is needed to correctly model the output stride
    return utils.mask_tensor(mask, a).contiguous()
