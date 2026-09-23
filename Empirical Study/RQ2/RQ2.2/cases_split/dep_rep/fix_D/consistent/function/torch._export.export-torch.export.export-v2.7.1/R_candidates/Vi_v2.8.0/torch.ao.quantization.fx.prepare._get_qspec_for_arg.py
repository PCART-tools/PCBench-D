def _get_qspec_for_arg(
    arg: Node,
    input_qspec_map: dict[Node, QuantizationSpecBase],
    named_modules: dict[str, torch.nn.Module],
) -> Optional[QuantizationSpecBase]:
    while _is_activation_post_process_node(arg, named_modules):
        arg = arg.args[0]  # type: ignore[assignment]
    return input_qspec_map.get(arg, None)
