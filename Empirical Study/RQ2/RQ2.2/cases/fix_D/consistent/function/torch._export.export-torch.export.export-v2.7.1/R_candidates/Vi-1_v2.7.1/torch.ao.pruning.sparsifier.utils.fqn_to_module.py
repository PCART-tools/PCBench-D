def fqn_to_module(model: Optional[nn.Module], path: str) -> Optional[nn.Module]:
    """
    Given an fqn, returns the corresponding module or tensor or None if the fqn given by `path`
    doesn't correspond to anything. Similar to model.get_submodule(path) but works for tensors.
    """
    if path != "":
        for name in path.split("."):
            model = getattr(model, name, None)
    return model
