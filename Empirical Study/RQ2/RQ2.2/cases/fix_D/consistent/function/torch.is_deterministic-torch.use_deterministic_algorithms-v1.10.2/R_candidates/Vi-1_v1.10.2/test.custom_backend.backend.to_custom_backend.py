def to_custom_backend(module):
    """
    This is a helper that wraps torch._C._jit_to_test_backend and compiles
    only the forward method with an empty compile spec.

    Args:
        module: input ScriptModule.

    Returns:
        The module, lowered so that it can run on TestBackend.
    """
    lowered_module = torch._C._jit_to_backend("custom_backend", module, {"forward": {"": ""}})
    return lowered_module
