def quantize_activation_fw(graph: torch.fx.Graph) -> None:
    output = graph.find_nodes(op="output")[0]
    fwd_outputs = output.args[0]
    quant_type = get_quant_type()
    clamp_min, clamp_max = calculate_range(quant_type)
    node_to_quant = dict()
    tensor_scale_nodes, sym_scale_nodes = [], []
    for node in fwd_outputs:
        # check if the activation node is the node saved for quantization
        if node.meta.get("saved_for_quantization", False):
            # case: use scaling
            if torch._inductor.config.post_grad_fusion_options[
                "activation_quantization_aten_pass"
            ].get("use_scaling", True):
                # calculating the scale
                scale_node = calculate_quantization_scaling(
                    graph, node, clamp_max, 1e-12
                )
                # converting to fp8
                quant_node = perform_quantization(
                    graph, node, scale_node, quant_type, clamp_min, clamp_max
                )
                if not is_sym_node(scale_node):
                    tensor_scale_nodes.append(scale_node)
                else:
                    sym_scale_nodes.append(scale_node)
            else:
                # case: do not use scaling
                with graph.inserting_after(node):
                    quant_node = graph.call_function(
                        torch.ops.prims.convert_element_type.default,
                        args=(node, quant_type),
                        name="fp8_quant_" + str(node.name),
                    )
                    quant_node.meta[
                        "val"
                    ] = torch.ops.prims.convert_element_type.default(
                        node.meta["val"], quant_type
                    )
                    quant_node.meta["tensor_meta"] = extract_tensor_metadata(
                        quant_node.meta["val"]
                    )
            node_to_quant[node] = quant_node
    # only update the return node args, and remain all other users unchanged
    output_updated_args = [
        node_to_quant[node] if node in node_to_quant else node for node in fwd_outputs  # type: ignore[union-attr]
    ]
    # add the scale nodes to the ouput find the first sym_node in the output
    idx = find_first_sym_node(output_updated_args)
    scale_nodes = tensor_scale_nodes + sym_scale_nodes
    if scale_nodes:
        output_updated_args = (
            output_updated_args[:idx] + scale_nodes + output_updated_args[idx:]
        )

    output.update_arg(0, tuple(output_updated_args))
    counters["inductor"]["activation_quantization_fwd_aten_pass"] += 1
