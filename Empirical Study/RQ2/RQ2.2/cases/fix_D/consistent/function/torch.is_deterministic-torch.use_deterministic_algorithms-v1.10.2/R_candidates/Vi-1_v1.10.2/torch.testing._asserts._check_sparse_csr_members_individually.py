def _check_sparse_csr_members_individually(
    check_tensors: Callable[..., Optional[_TestingErrorMeta]]
) -> Callable[..., Optional[_TestingErrorMeta]]:
    """Decorates strided tensor check functions to individually handle sparse CSR members.

    If the inputs are not sparse CSR, this decorator is a no-op.

    Args:
        check_tensors (Callable[[Tensor, Tensor], Optional[Exception]]): Tensor check function for strided
        tensors.
    """

    @functools.wraps(check_tensors)
    def wrapper(
        actual: Tensor,
        expected: Tensor,
        msg: Optional[Union[str, Callable[[Tensor, Tensor, Diagnostics], str]]] = None,
        **kwargs: Any,
    ) -> Optional[_TestingErrorMeta]:
        if not actual.is_sparse_csr:
            return check_tensors(actual, expected, msg=msg, **kwargs)

        kwargs_equal = dict(kwargs, rtol=0, atol=0)
        error_meta = check_tensors(
            actual.crow_indices(),
            expected.crow_indices(),
            msg=msg or functools.partial(_make_mismatch_msg, identifier="Sparse CSR crow_indices"),
            **kwargs_equal,
        )
        if error_meta:
            return error_meta

        error_meta = check_tensors(
            actual.col_indices(),
            expected.col_indices(),
            msg=msg or functools.partial(_make_mismatch_msg, identifier="Sparse CSR col_indices"),
            **kwargs_equal,
        )
        if error_meta:
            return error_meta

        error_meta = check_tensors(
            actual.values(),
            expected.values(),
            msg=msg or functools.partial(_make_mismatch_msg, identifier="Sparse CSR values"),
            **kwargs,
        )
        if error_meta:
            return error_meta

        return None

    return wrapper
