def create_getattr_from_value(module: torch.nn.Module, graph: Graph, prefix: str, value: Any) -> Node:
    """
    Given a value of any type, creates a getattr node corresponding to the value and
    registers the value as a buffer to the module.
    """
    get_new_attr_name = get_new_attr_name_with_prefix(prefix)
    attr_name = get_new_attr_name(module)
    device = assert_and_get_unique_device(module)
    module.register_buffer(attr_name, torch.tensor(value, device=device))
    # Create get_attr with value
    attr_node = graph.create_node("get_attr", attr_name)
    return attr_node
