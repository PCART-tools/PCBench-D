def get_torch_function_hook_type(
    parent_module: Optional[torch.nn.Module],
    func: Callable,
) -> HookType:
    # the direct __dict__ accesses are for performance, because
    # the default `torch.nn.Module.__getattr__` has overhead.
    parent_module_has_qstate = parent_module is not None and \
        '_modules' in parent_module.__dict__ and \
        '_auto_quant_state' in parent_module.__dict__['_modules']
    needs_op_hooks = parent_module_has_qstate and \
        parent_module.__dict__['_modules']['_auto_quant_state'].cur_op_needs_hooks(func)  # type: ignore[union-attr, operator]

    if needs_op_hooks:
        return HookType.OP_HOOKS
    elif (
        parent_module_has_qstate and
        # do not attempt to dequantize the args to dequantize, as that will
        # lead to infinite recursion
        func != torch.Tensor.dequantize
    ):
        return HookType.ARG_DEQUANTS
    else:
        return HookType.NONE
