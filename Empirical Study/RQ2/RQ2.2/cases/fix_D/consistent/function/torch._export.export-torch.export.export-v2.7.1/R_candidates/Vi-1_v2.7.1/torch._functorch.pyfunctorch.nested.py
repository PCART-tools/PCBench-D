@contextlib.contextmanager
def nested(*contexts):
    with contextlib.ExitStack() as stack:
        for ctx in contexts:
            stack.enter_context(ctx)
        yield contexts
