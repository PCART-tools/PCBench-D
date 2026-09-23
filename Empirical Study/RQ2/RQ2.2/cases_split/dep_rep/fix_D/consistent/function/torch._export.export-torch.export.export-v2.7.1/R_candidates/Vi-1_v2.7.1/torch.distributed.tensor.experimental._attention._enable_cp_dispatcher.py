@contextlib.contextmanager
def _enable_cp_dispatcher() -> Generator[None, None, None]:
    """Enables DTensor dispatcher to dispatch SDPA to CP."""
    old_handlers = DTensor._op_dispatcher._custom_op_handlers
    DTensor._op_dispatcher._custom_op_handlers = {**old_handlers, **customized_ops}

    yield

    DTensor._op_dispatcher._custom_op_handlers = old_handlers
