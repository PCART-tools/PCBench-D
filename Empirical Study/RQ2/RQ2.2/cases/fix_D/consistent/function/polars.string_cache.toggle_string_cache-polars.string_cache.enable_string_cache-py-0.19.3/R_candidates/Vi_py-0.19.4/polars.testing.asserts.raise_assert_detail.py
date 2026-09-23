def raise_assert_detail(
    obj: str,
    detail: str,
    left: Any,
    right: Any,
    exc: AssertionError | None = None,
) -> NoReturn:
    """Raise a detailed assertion error."""
    __tracebackhide__ = True

    error_msg = textwrap.dedent(
        f"""\
        {obj} are different ({detail})
        [left]:  {left}
        [right]: {right}\
        """
    )

    raise AssertionError(error_msg) from exc
