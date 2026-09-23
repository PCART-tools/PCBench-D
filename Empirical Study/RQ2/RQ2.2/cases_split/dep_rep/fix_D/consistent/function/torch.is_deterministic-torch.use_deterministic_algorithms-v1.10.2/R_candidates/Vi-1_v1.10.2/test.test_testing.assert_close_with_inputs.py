def assert_close_with_inputs(actual: Any, expected: Any) -> Iterator[Callable]:
    """Yields :func:`torch.testing.assert_close` with predefined positional inputs based on two examples.

    .. note::

        Every test that does not test for a specific input should iterate over this to maximize the coverage.

    Args:
        actual (Any): Actual input.
        expected (Any): Expected input.

    Yields:
        Callable: :func:`torch.testing.assert_close` with predefined positional inputs.
    """
    for inputs in make_assert_close_inputs(actual, expected):
        yield functools.partial(torch.testing.assert_close, *inputs)
