@compatibility(is_backward_compatible=False)
@contextmanager
def preserve_node_meta(enable=True):
    global should_preserve_node_meta
    global current_meta
    # If enable is False, this context manager is a no-op
    if not enable:
        yield
    else:
        saved_should_preserve_node_meta = should_preserve_node_meta
        # Shallow copy is OK since fields of current_meta are not mutated
        saved_current_meta = current_meta.copy()
        try:
            should_preserve_node_meta = True
            yield
        finally:
            should_preserve_node_meta = saved_should_preserve_node_meta
            current_meta = saved_current_meta
