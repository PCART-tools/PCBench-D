def is_torch_sym(value):
    return isinstance(value, (torch.SymBool, torch.SymInt)) and not isinstance(
        value.node, torch.nested._internal.nested_int.NestedIntNode
    )
