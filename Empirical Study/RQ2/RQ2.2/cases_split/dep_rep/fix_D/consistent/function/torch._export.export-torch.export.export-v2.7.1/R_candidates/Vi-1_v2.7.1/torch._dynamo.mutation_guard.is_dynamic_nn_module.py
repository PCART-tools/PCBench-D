def is_dynamic_nn_module(obj: Any, is_export: bool) -> bool:
    """Check for nn.Modules() created dynamically or mutated"""
    if isinstance(obj, torch.nn.Module) and (
        "forward" in obj.__dict__ or isinstance(obj, (dict, MutableMapping))
    ):
        # A monkey patched `.forward` indicates something wacky is going on
        # Similarly a nn module also subclassed as a dict is unusual.
        return True
    if hasattr(obj, "torchdynamo_force_dynamic"):
        return obj.torchdynamo_force_dynamic
    # For export, we will have to fix
    # 1) Input signature problem because params are lifted as inputs
    # 2) nn module stack info changes
    # 3) adjust failing tests
    if (
        isinstance(obj, torch.nn.Module)
        and config.inline_inbuilt_nn_modules
        and not is_export
    ):
        return True

    if isinstance(obj, torch.nn.Module) and nn_module_has_global_hooks():
        return True
    dyn = GenerationTracker.dynamic_classes.get(type(obj)) or GenerationTracker.check(
        obj
    )
    return dyn
