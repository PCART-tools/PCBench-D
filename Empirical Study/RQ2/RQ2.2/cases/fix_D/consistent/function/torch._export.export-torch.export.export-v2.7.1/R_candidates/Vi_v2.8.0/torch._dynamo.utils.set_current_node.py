@contextmanager
def set_current_node(node):
    old = get_current_node()
    _current_node.value = node
    try:
        yield
    finally:
        _current_node.value = old
