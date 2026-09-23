def is_lambda(lamb):
    LAMBDA = lambda: 0  # noqa: E731
    return isinstance(lamb, type(LAMBDA)) and lamb.__name__ == LAMBDA.__name__
