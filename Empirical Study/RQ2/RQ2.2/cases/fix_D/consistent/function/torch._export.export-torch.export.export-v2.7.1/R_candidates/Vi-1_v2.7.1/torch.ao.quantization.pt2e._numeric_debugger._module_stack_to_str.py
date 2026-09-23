def _module_stack_to_str(module_stack: object) -> str:
    """Simplifies the stack from ("mod", "mod.foo", "mod.foo.0", "mod.foo.0.linear")
    to "mod.foo.0.linear"
    """
    if not isinstance(module_stack, dict):
        return str(module_stack)
    module_values_list = list(module_stack.values())
    if len(module_values_list) > 0:
        owning_module = module_values_list[-1][0]
        return str(owning_module)
    else:
        return str(module_stack)
