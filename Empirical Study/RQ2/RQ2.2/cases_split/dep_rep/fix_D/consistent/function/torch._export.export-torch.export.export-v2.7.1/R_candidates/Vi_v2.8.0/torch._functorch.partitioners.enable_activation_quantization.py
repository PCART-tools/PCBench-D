def enable_activation_quantization(
    saved_values: list[fx.Node],
    fwd_module: fx.GraphModule,
    bwd_module: fx.GraphModule,
    static_lifetime_input_nodes: Optional[OrderedSet[fx.Node]] = None,
) -> None:
    if (
        inductor_config.post_grad_fusion_options.get(
            "activation_quantization_aten_pass", None
        )
        is None
    ):
        return

    static_input_names = (
        [node.name for node in static_lifetime_input_nodes]
        if static_lifetime_input_nodes
        else []
    )
    saved_values_names = {node.name: node for node in saved_values}
    if torch._inductor.config.post_grad_fusion_options[
        "activation_quantization_aten_pass"
    ].get("exclude_primals", False):
        saved_values_names = {
            node.name: node for node in saved_values if "primals" not in node.name
        }
    fwd_module_outputs = fwd_module.graph.find_nodes(op="output")[0].args[0]
    bwd_module_inputs = {
        node.name: node for node in bwd_module.graph.find_nodes(op="placeholder")
    }
    for node in fwd_module_outputs:
        if node.name in saved_values_names and should_quantize(node):
            if node.name in static_input_names:
                log.debug("Skipping quantization of static input %s: ", node.name)
                continue
            node.meta["saved_for_quantization"] = True
            node.meta["dequant_type"] = node.meta["val"].dtype
            # some of the fwd outputs and bwd inputs are not share the same object
            bwd_module_inputs[node.name].meta["saved_for_quantization"] = True
            bwd_module_inputs[node.name].meta["dequant_type"] = node.meta["val"].dtype

    trace_structured(
        "artifact",
        metadata_fn=lambda: {
            "name": "before_activation_quantization_fwd_aten_pass",
            "encoding": "string",
        },
        payload_fn=lambda: fwd_module.print_readable(
            print_output=False, include_stride=True, include_device=True
        ),
    )

    quantize_activation_fw(fwd_module.graph)

    trace_structured(
        "artifact",
        metadata_fn=lambda: {
            "name": "after_activation_quantization_fwd_aten_pass",
            "encoding": "string",
        },
        payload_fn=lambda: fwd_module.print_readable(
            print_output=False, include_stride=True, include_device=True
        ),
    )

    trace_structured(
        "artifact",
        metadata_fn=lambda: {
            "name": "before_activation_quantization_bwd_aten_pass",
            "encoding": "string",
        },
        payload_fn=lambda: bwd_module.print_readable(
            print_output=False, include_stride=True, include_device=True
        ),
    )

    quant_fwd_module_outputs = fwd_module.graph.find_nodes(op="output")[0].args[0]
    # update the corresponding bwd_inputs due to the fwd_outputs quantization
    for fwd_node in quant_fwd_module_outputs:
        if "fp8_quant_" in fwd_node.name:
            bwd_input = bwd_module_inputs[fwd_node.name.replace("fp8_quant_", "")]
            with bwd_module.graph.inserting_after(bwd_input):
                quant_bwd_input = bwd_module.graph.placeholder(name=fwd_node.name)
            dequant_type = bwd_input.meta["dequant_type"]
            quant_bwd_input.meta.update(fwd_node.meta)
            quant_bwd_input.meta["saved_for_quantization"] = True
            quant_bwd_input.meta["dequant_type"] = dequant_type
            bwd_input.replace_all_uses_with(quant_bwd_input)
            bwd_module.graph.erase_node(bwd_input)
    # update the bwd_inputs if quantization with scaling is used
    if torch._inductor.config.post_grad_fusion_options[
        "activation_quantization_aten_pass"
    ].get("use_scaling", True):
        quant_bwd_module_inputs = list(bwd_module.graph.find_nodes(op="placeholder"))
        # update the corresponding bwd input nodes find the last non-tangent node
        bwd_input_loc = quant_bwd_module_inputs[-1]
        for bw_input in reversed(quant_bwd_module_inputs):
            if not _is_tangent(bw_input):
                bwd_input_loc = bw_input
                break

        scaled_fwd_module_outputs = fwd_module.graph.find_nodes(op="output")[0].args[0]
        for fwd_node in scaled_fwd_module_outputs:
            if "fp8_scale_" in fwd_node.name:
                # fwd node is a scale node
                with bwd_module.graph.inserting_after(bwd_input_loc):
                    scale_bwd_input = bwd_module.graph.placeholder(name=fwd_node.name)
                scale_bwd_input.meta.update(fwd_node.meta)
                bwd_input_loc = scale_bwd_input

    quantize_activation_bw(bwd_module.graph)

    trace_structured(
        "artifact",
        metadata_fn=lambda: {
            "name": "after_activation_quantization_bwd_aten_pass",
            "encoding": "string",
        },
        payload_fn=lambda: bwd_module.print_readable(
            print_output=False, include_stride=True, include_device=True
        ),
    )
