def _module_stack_meta_from_node(
    node: torch.fx.Node, is_exported_program: bool = False
) -> _ModuleStackMeta:
    return _ModuleStackMeta(
        node.meta.get("nn_module_stack"), is_exported_program=is_exported_program
    )
