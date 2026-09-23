def get_module_hook_type(
    parent_module: Optional[torch.nn.Module],
    cur_module: torch.nn.Module,
) -> HookType:
    cached_hook_type = getattr(cur_module, '_auto_quant_module_hook_type', None)
    if cached_hook_type is not None:
        return cached_hook_type
    parent_module_has_qstate = parent_module is not None and \
        '_modules' in parent_module.__dict__ and \
        '_auto_quant_state' in parent_module.__dict__['_modules']
    needs_op_hooks = parent_module_has_qstate and \
        parent_module.__dict__['_modules']['_auto_quant_state'].cur_op_needs_hooks(cur_module)  # type: ignore[union-attr, operator]
    # We need IO hooks if
    # * we are calling forward on a module (always True here)
    # * that module has quant state
    # * that module does not need op hooks for the parent
    needs_io_hooks = (
        '_modules' in cur_module.__dict__ and
        '_auto_quant_state' in cur_module.__dict__['_modules'] and
        (not needs_op_hooks)
    )
    needs_arg_dequants = parent_module_has_qstate and not needs_op_hooks

    if needs_op_hooks:
        result = HookType.OP_HOOKS
    elif needs_io_hooks:
        result = HookType.MODULE_IO_HOOKS
    elif needs_arg_dequants:
        result = HookType.ARG_DEQUANTS
    else:
        result = HookType.NONE
    cur_module._auto_quant_module_hook_type = result  # type: ignore[assignment]
    return result
