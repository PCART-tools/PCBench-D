def remove(module, name):
    r"""Remove the pruning reparameterization from a module and the pruning method from the forward hook.

    The pruned parameter named ``name`` remains permanently pruned, and the parameter
    named ``name+'_orig'`` is removed from the parameter list. Similarly,
    the buffer named ``name+'_mask'`` is removed from the buffers.

    Note:
        Pruning itself is NOT undone or reversed!

    Args:
        module (nn.Module): module containing the tensor to prune
        name (str): parameter name within ``module`` on which pruning
            will act.

    Examples:
        >>> m = random_unstructured(nn.Linear(5, 7), name="weight", amount=0.2)
        >>> m = remove(m, name="weight")
    """
    for k, hook in module._forward_pre_hooks.items():
        if isinstance(hook, BasePruningMethod) and hook._tensor_name == name:
            hook.remove(module)
            del module._forward_pre_hooks[k]
            return module

    raise ValueError(
        f"Parameter '{name}' of module {module} has to be pruned before pruning can be removed"
    )
