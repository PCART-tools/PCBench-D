def has_torch_function(vt: torch._dynamo.variables.base.VariableTracker) -> bool:
    from torch._dynamo.variables import UserDefinedObjectVariable
    from torch._dynamo.variables.torch_function import TensorWithTFOverrideVariable

    # Note on lazy vars: The value will either be realized or not throughout the course of execution
    # if the value has a torch function, it will eventually be realized so we can realize it here
    # if the value does not have a torch function, it may or may not be realized
    # if it is realized it will be used and guards will be installed properly
    # if it is not used, guards won't be installed, and it doesn't matter
    # if the value has a torch function or not, so we should *not* realize it.
    # NB: We technically know that if is_realized is False, LazyVariableTracker has the peek_value method
    # but mypy does not unfortunately
    if vt.is_realized() or (
        hasattr(vt, "peek_value") and hasattr(vt.peek_value(), "__torch_function__")
    ):
        if isinstance(vt, TensorWithTFOverrideVariable):
            return True

        return isinstance(vt, UserDefinedObjectVariable) and hasattr(
            vt.value, "__torch_function__"
        )

    return False
