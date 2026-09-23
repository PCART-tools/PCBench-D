def _port_metadata_for_output_quant_nodes(
    node: torch.fx.Node, qspec: Optional[QuantizationSpecBase]
):
    if qspec is None:
        return

    node_users = _filter_sym_size_users(node)
    if len(node.users) == 0:
        return
    if len(node_users) != 1:
        logger.warning(f"Expecting {node} to have single user")  # noqa: G004
    q_node = node_users.pop()
    if q_node.op != "call_function" or q_node.target not in _QUANTIZE_OPS:
        logger.warning(
            f"Expecting {node} user to be a quantized op but got {q_node}"  # noqa: G004
        )  # noqa: G004
        return

    _add_metadata(q_node, node)
