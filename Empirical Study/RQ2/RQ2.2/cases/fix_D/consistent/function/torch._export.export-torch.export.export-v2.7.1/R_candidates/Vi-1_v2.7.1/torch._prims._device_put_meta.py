def _device_put_meta(
    a: TensorLikeType, device: Union[str, torch.device], non_blocking=False
) -> TensorLikeType:
    assert isinstance(a, TensorLike)
    assert isinstance(device, (str, torch.device))
    assert isinstance(non_blocking, bool)

    return TensorMeta(a, device=utils.canonicalize_device(device))
