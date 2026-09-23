@_trace_wrapped_op.py_impl(FakeTensorMode)
def inner_fake(*args: Any, **kwargs: Any) -> None:
    raise RuntimeError("This op should never be invoked here")
