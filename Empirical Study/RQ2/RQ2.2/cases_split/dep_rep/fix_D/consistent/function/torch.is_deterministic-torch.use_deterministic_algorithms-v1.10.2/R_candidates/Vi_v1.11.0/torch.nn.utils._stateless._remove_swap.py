def _remove_swap(module, name: str) -> None:
    if hasattr(module, "_orig_class"):
        module.__class__ = module._orig_class
        delattr(module, "_orig_class")
        delattr(module, "_functional_parameters")
