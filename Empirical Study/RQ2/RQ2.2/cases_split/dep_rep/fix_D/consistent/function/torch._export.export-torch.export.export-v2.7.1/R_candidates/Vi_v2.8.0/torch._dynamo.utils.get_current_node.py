def get_current_node():
    return getattr(_current_node, "value", None)
