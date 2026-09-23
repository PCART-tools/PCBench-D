def activation_is_memoryless(qconfig: QConfig):
    """
    Return whether the observer for activations defined in the given QConfig is memoryless.
    """
    def _is_memoryless(observer):
        return hasattr(observer, "memoryless") and observer.memoryless
    act = qconfig.activation()
    if isinstance(act, FakeQuantizeBase) and hasattr(act, "activation_post_process"):
        return _is_memoryless(act.activation_post_process)
    else:
        return _is_memoryless(act)
