def get_script_object(
    gm: torch.nn.Module, node: torch.fx.Node
) -> torch._C.ScriptObject:
    assert isinstance(node, torch.fx.Node)
    assert node.op == "get_attr"
    attr_name = node.target
    assert isinstance(attr_name, str)

    mod = gm
    for attr in attr_name.split("."):
        mod = getattr(mod, attr)
    assert isinstance(mod, torch._C.ScriptObject)
    return mod
