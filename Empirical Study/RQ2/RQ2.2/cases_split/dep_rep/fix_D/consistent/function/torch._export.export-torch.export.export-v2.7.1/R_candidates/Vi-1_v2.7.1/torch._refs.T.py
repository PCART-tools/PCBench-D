def T(a: TensorLikeType) -> TensorLikeType:
    # n != 2 && n != 0 is deprecated in regular PyTorch.
    torch._check(
        a.ndim in (0, 2),
        lambda: (
            "The use of `x.T` on tensors of dimension other than 0 or 2 "
            "to reverse their shape is not supported."
        ),
    )
    return a.t()
