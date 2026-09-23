@_disable_user_warnings
def get_overridable_functions() -> dict[Any, list[Callable]]:
    """List functions that are overridable via __torch_function__

    Returns
    -------
    Dict[Any, List[Callable]]
        A dictionary that maps namespaces that contain overridable functions
        to functions in that namespace that can be overridden.
    """
    return _get_overridable_functions()[0]
