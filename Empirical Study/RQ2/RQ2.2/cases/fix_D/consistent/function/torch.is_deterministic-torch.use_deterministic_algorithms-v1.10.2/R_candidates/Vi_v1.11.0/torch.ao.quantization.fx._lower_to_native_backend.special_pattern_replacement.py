def special_pattern_replacement(model: QuantizedGraphModule) -> QuantizedGraphModule:
    modules = dict(model.named_modules(remove_duplicate=False))
    nodes = list(model.graph.nodes)
    for n in model.graph.nodes:
        q_node = n
        if q_node.target == torch.quantize_per_tensor:
            # get output scale/zero_point/dtype from the quantize node
            ref_node, scale_node, zero_point_node, dtype = q_node.args

            is_call_function, is_call_method, is_call_module = check_node(ref_node, modules)
            if is_call_module or is_call_function or is_call_method:
                dq_node = ref_node.args[0]
                if dq_node.target == 'dequantize':
                    if is_call_module:
                        ref_module = modules[ref_node.target]
                        # change this pattern to use the corresponding quantized module
                        # replace reference module with quantized module
                        parent_name, module_name = _parent_name(ref_node.target)
                        setattr(modules[parent_name], module_name, ref_module)
                    else:
                        dq_node.target = ref_node

                    # remove dq node:
                    dq_node_input = dq_node.args[0]
                    dq_node.replace_all_uses_with(dq_node_input)
                    model.graph.erase_node(dq_node)

                    # remove q node and args:
                    q_node_input = q_node.args[0]
                    q_node.replace_all_uses_with(q_node_input)
                    model.graph.erase_node(q_node)
                    model.graph.erase_node(scale_node)
                    model.graph.erase_node(zero_point_node)


    model.recompile()
    return model
