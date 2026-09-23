def reset_optimizer_instance_count():
    """
    This function clears the _optimizer_instance_count. And keeps it
    empty. This functionality is needed in some situations where
    optimizer instance count might not reset even though the workplace is reset.
    """
    _optimizer_instance_count.clear()
