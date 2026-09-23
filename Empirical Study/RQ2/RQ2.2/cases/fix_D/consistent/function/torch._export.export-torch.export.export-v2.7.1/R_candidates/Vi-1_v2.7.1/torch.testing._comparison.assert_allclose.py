@deprecated(
    "`torch.testing.assert_allclose()` is deprecated since 1.12 and will be removed in a future release. "
    "Please use `torch.testing.assert_close()` instead. "
    "You can find detailed upgrade instructions in https://github.com/pytorch/pytorch/issues/61844.",
    category=FutureWarning,
)
def assert_allclose(
    actual: Any,
    expected: Any,
    rtol: Optional[float] = None,
    atol: Optional[float] = None,
    equal_nan: bool = True,
    msg: str = "",
) -> None:
    """
    .. warning::

       :func:`torch.testing.assert_allclose` is deprecated since ``1.12`` and will be removed in a future release.
       Please use :func:`torch.testing.assert_close` instead. You can find detailed upgrade instructions
       `here <https://github.com/pytorch/pytorch/issues/61844>`_.
    """
    if not isinstance(actual, torch.Tensor):
        actual = torch.tensor(actual)
    if not isinstance(expected, torch.Tensor):
        expected = torch.tensor(expected, dtype=actual.dtype)

    if rtol is None and atol is None:
        rtol, atol = default_tolerances(
            actual,
            expected,
            dtype_precisions={
                torch.float16: (1e-3, 1e-3),
                torch.float32: (1e-4, 1e-5),
                torch.float64: (1e-5, 1e-8),
            },
        )

    torch.testing.assert_close(
        actual,
        expected,
        rtol=rtol,
        atol=atol,
        equal_nan=equal_nan,
        check_device=True,
        check_dtype=False,
        check_stride=False,
        msg=msg or None,
    )
