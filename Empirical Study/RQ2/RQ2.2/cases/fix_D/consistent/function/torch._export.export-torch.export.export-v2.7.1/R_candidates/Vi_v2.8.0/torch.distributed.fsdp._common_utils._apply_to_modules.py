def _apply_to_modules(
    root_module: torch.nn.Module,
    module_fn: Callable,
    return_fn: Callable,
    filter_fqns: Optional[list[str]] = None,
    *args,
    **kwargs,
):
    """
    Performs a pre-order traversal of the modules in the hierarchy rooted at
    ``root_module``, applying ``module_fn`` at each module and finally
    returning a value using ``return_fn``. The traversal constructs the full
    module prefix name (e.g. "module.submodule." just like in model state dict)
    and makes that available to ``module_fn``.

    ``filter_fqns`` is used because some module may have its own prefix similar
    to ``FullyShardedDataParallel`` and the ``named_parameters()`` is overwritten
    to remove the prefix.
    """

    def f(module: torch.nn.Module, prefix: str, tree_level: int, *args, **kwargs):
        # Call the module function before recursing over children (pre-order)
        module_fn(module, prefix, tree_level, *args, **kwargs)
        for submodule_name, submodule in module.named_children():
            if submodule is None:
                continue
            new_prefix = prefix + submodule_name + "."
            new_tree_level = tree_level + 1
            if filter_fqns is not None:
                for fqn in filter_fqns:
                    if fqn.startswith(new_prefix):
                        break
                else:
                    # DMP's named_parameter() will mess up the traversal with
                    # ``named_children`` + `named_parameter(recurse=False)``.
                    # This hack is a must to make the traversal work.
                    # TODO: Remove this hack once DMP + FSDP is not supported.
                    # It turns out that recursive wrapping may trigger this as
                    # well.
                    if (
                        submodule_name == "_fsdp_wrapped_module"
                        or submodule_name == "_dmp_wrapped_module"
                    ):
                        new_prefix = prefix
                    elif submodule_name == "module":
                        new_prefix = prefix
            f(submodule, new_prefix, new_tree_level, *args, **kwargs)

    f(root_module, "", 0, *args, **kwargs)
    return return_fn(*args, **kwargs)
