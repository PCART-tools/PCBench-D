def is_tensor(ann):
    if issubclass(ann, torch.Tensor):
        return True

    if issubclass(
        ann,
        (
            torch.LongTensor,
            torch.DoubleTensor,
            torch.FloatTensor,
            torch.IntTensor,
            torch.ShortTensor,
            torch.HalfTensor,
            torch.CharTensor,
            torch.ByteTensor,
            torch.BoolTensor,
        ),
    ):
        warnings.warn(
            "TorchScript will treat type annotations of Tensor "
            "dtype-specific subtypes as if they are normal Tensors. "
            "dtype constraints are not enforced in compilation either."
        )
        return True

    return False
