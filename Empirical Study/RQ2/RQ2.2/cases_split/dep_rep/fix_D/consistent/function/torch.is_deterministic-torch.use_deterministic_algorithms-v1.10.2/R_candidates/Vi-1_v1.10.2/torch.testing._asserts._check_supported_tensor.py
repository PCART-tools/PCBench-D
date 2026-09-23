def _check_supported_tensor(input: Tensor) -> Optional[_TestingErrorMeta]:
    """Checks if the tensor is supported by the current infrastructure.

    Returns:
        (Optional[_TestingErrorMeta]): If check did not pass.
    """
    if input.layout not in {torch.strided, torch.sparse_coo, torch.sparse_csr}:  # type: ignore[attr-defined]
        return _TestingErrorMeta(ValueError, f"Unsupported tensor layout {input.layout}")

    return None
