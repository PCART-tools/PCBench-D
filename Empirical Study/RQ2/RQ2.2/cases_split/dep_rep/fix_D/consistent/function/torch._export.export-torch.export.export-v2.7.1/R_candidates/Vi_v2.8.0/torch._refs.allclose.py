def allclose(
    a: TensorLikeType,
    b: TensorLikeType,
    rtol: float = 1e-05,
    atol: float = 1e-08,
    equal_nan: bool = False,
) -> bool:
    """
    Reference implementation of torch.allclose
    """
    _check_close_args(name="torch.allclose", a=a, b=b, rtol=rtol, atol=atol)

    return bool(
        torch.all(torch.isclose(a, b, rtol=rtol, atol=atol, equal_nan=equal_nan)).item()
    )
