@typing.no_type_check
def _sticky_export(forward_func, dynamic_shapes_callback=None):
    """
    Lazily export the model on first forward call.
    Usage:
        model.forward = _sticky_export(model.forward, dynamic_shapes_callback=callback)
    """
    model = forward_func.__self__
    original_forward = forward_func.__func__

    @functools.wraps(forward_func)
    def wrapper(*args, **kwargs):
        # Unpatch forward to avoid recursion during export
        model.forward = types.MethodType(original_forward, model)

        dynamic_shapes_spec = None
        if dynamic_shapes_callback:
            dynamic_shapes_spec = dynamic_shapes_callback(*args, **kwargs)

        try:
            exported = torch.export.export(
                model,
                args,
                kwargs,
                dynamic_shapes=dynamic_shapes_spec,
            ).module()
            wrapper._exported_artifact = exported
        finally:
            # Restore the wrapper after export
            model.forward = wrapper

        return exported(*args, **kwargs)

    return wrapper
