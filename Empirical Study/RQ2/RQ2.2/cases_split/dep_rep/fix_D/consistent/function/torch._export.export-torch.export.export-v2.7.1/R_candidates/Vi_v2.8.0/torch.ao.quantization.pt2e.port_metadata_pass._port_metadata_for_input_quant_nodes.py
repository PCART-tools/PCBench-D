def _port_metadata_for_input_quant_nodes(
    input_node: torch.fx.Node,
    node: torch.fx.Node,
    qspec: Optional[QuantizationSpecBase],
):
    if qspec is None:
        return

    is_dynamic_quant = getattr(qspec, "is_dynamic", None)
    if is_dynamic_quant is not None and is_dynamic_quant is True:
        choose_qparams_node = _find_choose_qparams_node(input_node)
        if choose_qparams_node is None:
            raise ValueError(f"No chose qparams node found for {node}")
        choose_qparam_users = _filter_sym_size_users(choose_qparams_node)
        if len(choose_qparam_users) != 2:
            raise InternalError(f"Expecting exactly two user for {choose_qparams_node}")
        scale_node = choose_qparam_users.pop()
        dynamic_q_node = next(iter(scale_node.users.keys()))
        dynamic_q_node_users = _filter_sym_size_users(dynamic_q_node)
        if len(dynamic_q_node_users) > 1:
            raise InternalError(f"Expecting single user for {dynamic_q_node}")
        dynamic_dq_node = dynamic_q_node_users.pop()
        _add_metadata(choose_qparams_node, node)
        _add_metadata(dynamic_q_node, node)
        _add_metadata(dynamic_dq_node, node)
    else:
        q_node, dq_node = _find_q_dq_node_for_user(input_node, node)
        if q_node is None or dq_node is None:
            return
        # add metadata for all the node between q_node and get_attr node
        # if the q_node can be traced back to get_attr node
        q_to_get_attr_nodes = [q_node]
        q_node_input = q_node.args[0]
        while (
            isinstance(q_node_input, torch.fx.Node)
            and q_node_input.op == "call_function"
            and q_node_input.target
            in [
                torch.ops.aten.flatten.using_ints,
                torch.ops.aten.permute.default,
                torch.ops.aten.permute_copy.default,
                torch.ops.aten.slice_copy.Tensor,
                torch.ops.aten.squeeze.dim,
                torch.ops.aten.squeeze_copy.dim,
                torch.ops.aten.transpose.Dimname,
                torch.ops.aten.transpose.int,
                torch.ops.aten.transpose_,
                torch.ops.aten.view_copy.default,
                torch.ops.aten.view.default,
                torch.ops.aten._mkldnn_transpose,
            ]
        ):
            q_to_get_attr_nodes.append(q_node_input)
            q_node_input = q_node_input.args[0]
        if isinstance(q_node_input, torch.fx.Node) and q_node_input.op == "get_attr":
            for n in q_to_get_attr_nodes:
                _add_metadata(n, q_node_input)
        _add_metadata(dq_node, node)
