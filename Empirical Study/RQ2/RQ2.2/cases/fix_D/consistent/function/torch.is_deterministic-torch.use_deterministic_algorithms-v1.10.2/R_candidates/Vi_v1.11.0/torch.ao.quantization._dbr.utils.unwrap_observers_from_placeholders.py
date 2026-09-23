def unwrap_observers_from_placeholders(module: torch.nn.Module) -> None:
    """
    Restores observers back to their original state.
    """
    # Note: we cannot use module.named_children() because we can
    # have two different names refer to the same module, for example
    # when we are reusing observers for torch.add scalar version.
    for name, child in module._modules.items():
        if child is None:
            continue
        if isinstance(child, ObserverWrapper):
            unwrapped = child.child
            setattr(module, name, unwrapped)
        else:
            unwrap_observers_from_placeholders(child)
