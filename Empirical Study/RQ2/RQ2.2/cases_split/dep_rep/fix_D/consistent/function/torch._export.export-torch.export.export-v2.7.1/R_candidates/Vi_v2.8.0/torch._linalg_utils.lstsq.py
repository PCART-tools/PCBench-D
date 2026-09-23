def lstsq(input: Tensor, A: Tensor, *, out=None) -> tuple[Tensor, Tensor]:
    raise RuntimeError(
        "This function was deprecated since version 1.9 and is now removed. "
        "`torch.lstsq` is deprecated in favor of `torch.linalg.lstsq`.\n"
        "`torch.linalg.lstsq` has reversed arguments and does not return the QR decomposition in "
        "the returned tuple (although it returns other information about the problem).\n\n"
        "To get the QR decomposition consider using `torch.linalg.qr`.\n\n"
        "The returned solution in `torch.lstsq` stored the residuals of the solution in the "
        "last m - n columns of the returned value whenever m > n. In torch.linalg.lstsq, "
        "the residuals are in the field 'residuals' of the returned named tuple.\n\n"
        "The unpacking of the solution, as in\n"
        "X, _ = torch.lstsq(B, A).solution[:A.size(1)]\n"
        "should be replaced with:\n"
        "X = torch.linalg.lstsq(A, B).solution"
    )
