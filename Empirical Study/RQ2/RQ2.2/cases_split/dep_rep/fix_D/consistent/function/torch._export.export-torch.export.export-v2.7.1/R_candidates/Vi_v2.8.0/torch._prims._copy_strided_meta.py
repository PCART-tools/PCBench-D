def _copy_strided_meta(a: TensorLikeType, stride: ShapeType):
    assert isinstance(a, TensorLike)
    return torch.empty_strided(
        a.shape,
        stride,
        dtype=a.dtype,
        layout=a.layout,
        device=a.device,
        requires_grad=a.requires_grad,
    )
