@register_decomposition(aten.select_scatter)
@out_wrapper()
def select_scatter(x: TensorLikeType, src: TensorLikeType, dim: int, index: int):
    dim = utils.canonicalize_dim(x.ndim, dim)
    mask_shape = [1] * x.ndim
    mask_shape[dim] = -1
    if index < 0:
        index = index + x.shape[dim]
    mask = torch.arange(x.shape[dim], device=x.device).view(mask_shape) == index
    src = torch.unsqueeze(src, dim).expand(x.shape)
    return torch.where(mask, src, x)
