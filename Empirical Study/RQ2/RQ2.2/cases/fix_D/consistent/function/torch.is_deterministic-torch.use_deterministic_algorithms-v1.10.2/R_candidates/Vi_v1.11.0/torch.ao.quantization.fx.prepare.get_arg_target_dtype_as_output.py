def get_arg_target_dtype_as_output(
    arg: Node,
    modules: Dict[str, torch.nn.Module],
    node_name_to_target_dtype: Dict[str, Dict[str, Optional[torch.dtype]]],
) -> Optional[torch.dtype]:
    """ Get the target output activation dtype for
    the argumnet in the original graph, skipping inserted observers
    We are assuming that the observers are inserted correctly, and the dtype for
    argument in quantized graph will match what is specified by the qconfig
    """
    assert isinstance(arg, Node)
    if is_activation_post_process_node(arg, modules):
        observed_arg = arg.args[0]
        assert isinstance(observed_arg, Node), "Currently we only support observing Node"
        return node_name_to_target_dtype[observed_arg.name]["output_activation_dtype"]
    else:
        return node_name_to_target_dtype[arg.name]["output_activation_dtype"]
