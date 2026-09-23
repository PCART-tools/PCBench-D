def _check_sparse_coo_members_individually(
    check_tensors: Callable[..., Optional[_TestingErrorMeta]]
) -> Callable[..., Optional[_TestingErrorMeta]]:
    """Decorates strided tensor check functions to individually handle sparse COO members.

    If the inputs are not sparse COO, this decorator is a no-op.

    Args:
        check_tensors (Callable[[Tensor, Tensor], Optional[Exception]]): Tensor check function for strided tensors.
    """

    @functools.wraps(check_tensors)
    def wrapper(
        actual: Tensor,
        expected: Tensor,
        msg: Optional[Union[str, Callable[[Tensor, Tensor, Diagnostics], str]]] = None,
        **kwargs: Any,
    ) -> Optional[_TestingErrorMeta]:
        if not actual.is_sparse:
            return check_tensors(actual, expected, msg=msg, **kwargs)

        if actual._nnz() != expected._nnz():
            return _TestingErrorMeta(
                AssertionError,
                (
                    f"The number of specified values in sparse COO tensors does not match: "
                    f"{actual._nnz()} != {expected._nnz()}"
                ),
            )

        kwargs_equal = dict(kwargs, rtol=0, atol=0)
        error_meta = check_tensors(
            actual._indices(),
            expected._indices(),
            msg=msg or functools.partial(_make_mismatch_msg, identifier="Sparse COO indices"),
            **kwargs_equal,
        )
        if error_meta:
            return error_meta

        error_meta = check_tensors(
            actual._values(),
            expected._values(),
            msg=msg or functools.partial(_make_mismatch_msg, identifier="Sparse COO values"),
            **kwargs,
        )
        if error_meta:
            return error_meta

        return None

    return wrapper
