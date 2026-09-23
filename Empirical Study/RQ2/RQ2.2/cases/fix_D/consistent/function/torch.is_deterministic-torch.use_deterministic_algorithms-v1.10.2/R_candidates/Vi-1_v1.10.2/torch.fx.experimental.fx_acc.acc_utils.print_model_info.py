def print_model_info(gm: torch.fx.GraphModule, header: Optional[str] = None):
    """
    Print out info of the provided `gm`.
    If `header` is provided then it's included in the printed string.
    """
    ops_and_counts: Dict[Callable, int] = dict()
    placeholder_count = get_attr_count = call_method_count = call_module_count = 0
    for node in gm.graph.nodes:
        if node.op == "call_function":
            ops_and_counts[node.target] = ops_and_counts.get(node.target, 1) + 1
        elif node.op == "placeholder":
            placeholder_count += 1
        elif node.op == "get_attr":
            get_attr_count += 1
        elif node.op == "call_method":
            call_method_count += 1
        elif node.op == "call_module":
            call_module_count += 1
        elif node.op == "output":
            output_count = len(node.args[0]) if isinstance(node.args[0], tuple) else 1
        else:
            raise RuntimeError(f"Unknown node found: {node.format_node()}")

    header = "" if header is None else f" [{header}]"
    model_info_str = f"Model Info{header}:\n"
    model_info_str += f"> placeholder: {placeholder_count}\n"
    model_info_str += f"> get_attr: {get_attr_count}\n"
    model_info_str += f"> output: {output_count}\n"
    if call_module_count != 0:
        model_info_str += f"> WARNING: call_module: {call_module_count}"
    if call_method_count != 0:
        model_info_str += f"> WARNING: call_method: {call_method_count}"

    # Sort and print all the other ops. Sort so it's deterministic between runs and
    # easier to parse.
    pretty_ops_and_counts: List[Tuple[str, int]] = []
    for op, count in ops_and_counts.items():
        pretty_ops_and_counts.append((_get_qualified_name(op), count))
    pretty_ops_and_counts.sort()
    for op_str, count in pretty_ops_and_counts:
        model_info_str += f"> {op_str}: {count}\n"

    print(model_info_str)
