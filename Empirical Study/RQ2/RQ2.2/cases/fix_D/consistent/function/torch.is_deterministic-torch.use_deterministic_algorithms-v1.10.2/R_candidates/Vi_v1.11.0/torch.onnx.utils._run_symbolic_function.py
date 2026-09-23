def _run_symbolic_function(g, block, n, inputs, env, operator_export_type=OperatorExportTypes.ONNX):
    # NB: Returning None means the node gets cloned as is into
    # the new graph
    try:
        import torch
        from torch.onnx.symbolic_helper import _export_onnx_opset_version as opset_version
        import torch.onnx.symbolic_registry as sym_registry

        sym_registry.register_version("", opset_version)

        # Quantized op symbolics are registered for opset 9 only.
        if operator_export_type == OperatorExportTypes.ONNX_ATEN_FALLBACK and opset_version == 9:
            import torch.onnx.symbolic_caffe2
            torch.onnx.symbolic_caffe2.register_quantized_ops("caffe2", opset_version)

        # See Note [Export inplace]
        # TODO: I think this is not necessary anymore
        if n.kind().endswith("_"):
            ns_op_name = n.kind()[:-1]
        else:
            ns_op_name = n.kind()
        ns, op_name = ns_op_name.split("::")
        if ns == "onnx":
            if op_name == "Placeholder":
                return torch._C._jit_onnx_convert_pattern_from_subblock(block, n, env)
            else:
                # Use the original node directly
                attrs = {k + "_" + n.kindOf(k)[0]: n[k] for k in n.attributeNames()}
                return g.op(op_name, *inputs, **attrs, outputs=n.outputsSize())

        elif ns == "aten":
            is_exportable_aten_op = sym_registry.is_registered_op(op_name, "", opset_version)
            is_onnx_aten_export = operator_export_type == OperatorExportTypes.ONNX_ATEN
            is_aten_fallback_export = operator_export_type == OperatorExportTypes.ONNX_ATEN_FALLBACK
            if is_onnx_aten_export or (not is_exportable_aten_op and is_aten_fallback_export):
                # Direct ATen export requested
                attrs = {k + "_" + n.kindOf(k)[0]: n[k] for k in n.attributeNames()}
                outputs = n.outputsSize()
                attrs["outputs"] = outputs
                return _graph_at(g, op_name, *inputs, aten=True, **attrs)
            else:
                # Export it regularly
                domain = ""
                symbolic_fn = _find_symbolic_in_registry(domain, op_name, opset_version, operator_export_type)
                if symbolic_fn is None:
                    return None
                attrs = {k: n[k] for k in n.attributeNames()}
                return symbolic_fn(g, *inputs, **attrs)

        elif ns == "prim":
            if op_name == "Constant" and not n.mustBeNone():
                if n.kindOf("value") == "t":
                    return g.op("Constant", value_t=n["value"])
                if n.kindOf("value") == "s":
                    return g.op("Constant", value_s=n["value"])
                elif n.output().type().isSubtypeOf(ListType.ofInts()) or n.output().type().isSubtypeOf(ListType.ofFloats()):
                    vals = n.output().toIValue()
                    value = torch.stack([torch.tensor(v) for v in vals]) if len(vals) else []
                    return g.op("Constant", value_t=value)
                elif n.output().type().kind() == "DeviceObjType":
                    return None
                else:
                    raise RuntimeError("Unsupported prim::Constant kind: `{}`. Send a bug report.".format(
                        n.kindOf("value")))
            elif n.mustBeNone() or op_name == "ListConstruct" or op_name == "ListUnpack" or op_name == "Uninitialized":
                # None is not an ONNX operator; keep it as None
                # Let the exporter handle and finally eliminate these ops
                # ListConstruct and ListUnpack will be erased in the ONNX peephole pass
                # Uninitialized will be erased during shape/type inference
                return None
            elif op_name == "device" and n.output().type().kind() == "DeviceObjType":
                return None
            elif op_name == "Loop" or op_name == "If":
                static_if = (op_name == "If" and inputs[0].node().kind() == "onnx::Constant")
                is_sub_block = False
                if static_if:
                    # Fold static if
                    #
                    # The torch IR
                    # graph(%embedding_matrix.1 : Float(10, 15, strides=[15, 1], requires_grad=0, device=cpu),
                    #    %input.1 : Long(6, strides=[1], requires_grad=0, device=cpu), ...
                    # %65 : Bool(requires_grad=0, device=cpu) = prim::Constant[value={0}]()
                    # %21 : Long(device=cpu) = aten::eq(%20, %64)
                    # %22 : Long(device=cpu) = prim::If(%21)
                    #     block0():
                    #     %23 : Long(device=cpu) = aten::is_floating_point(%input.1)
                    #     -> (%23)
                    #     block1():
                    #     -> (%65)
                    # %input.53 : Tensor, %weight : Tensor = prim::If(%22)
                    #     block0():
                    #     -> (%embedding_matrix.1, %input.1)
                    #     block1():
                    #     -> (%input.1, %embedding_matrix.1)
                    # %26 : int[] = aten::size(%input.53)
                    #
                    # The converted ONNX graph
                    # %10 : Bool(device=cpu) = onnx::Constant[value={0}]()
                    # %14 : Bool(device=cpu) = onnx::Equal(%13, %8)
                    # %15 : Bool(requires_grad=0, device=cpu) = onnx::Constant[value={0}]()
                    # %16 : Long(1, strides=[1], device=cpu) = onnx::Shape(%input.1)
                    input_flag = inputs[0].node()['value'].tolist()
                    const_value = all(input_flag) if isinstance(input_flag, list) else bool(input_flag)
                    block_idx = 0 if const_value else 1
                    current_b = list(n.blocks())[block_idx]
                    is_sub_block = True
                    env = torch._C._jit_pass_onnx_block(current_b, block, operator_export_type, env,
                                                        is_sub_block)
                    if_output_list = list(n.outputs())
                    current_b_list = list(current_b.outputs())

                    final_b_list = []
                    for idx in range(len(if_output_list)):
                        if current_b_list[idx] not in env:
                            raise RuntimeError("The sub block ATen output " + current_b_list[idx] + " is not in env.")
                        onnx_b = env[current_b_list[idx]]
                        final_b_list.append(onnx_b)
                    return final_b_list
                else:
                    new_op_outputs = g.op(op_name, *inputs, outputs=n.outputsSize())
                    new_node = new_op_outputs[0].node() if n.outputsSize() > 1 else new_op_outputs.node()
                    for b in n.blocks():
                        new_block = new_node.addBlock()
                        # Copy input metadata to subblock
                        #
                        # If format:
                        #   prim::If(cond)
                        #     block0()
                        #     block1()
                        #
                        # Loop format:
                        #   prim::Loop(iter, cond, input_1, ..., input_n)
                        #     block0(iter, input_1, ..., input_n)
                        #
                        # For `If` node, there is nothing to copy.
                        # For `Loop` node, copy metadata for `iter`, `input_1`, ..., `input_n`.
                        for i, b_in in enumerate(b.inputs()):
                            if i == 0 and i < len(inputs):
                                b_in.setType(inputs[i].type())
                            if i > 0 and (i + 1) < len(inputs):
                                b_in.setType(inputs[i + 1].type())
                        torch._C._jit_pass_onnx_block(b, new_block, operator_export_type, env,
                                                      is_sub_block)
                    new_op_outputs = torch._C._jit_pass_fixup_onnx_controlflow_node(new_node, opset_version)
                    # Process Loop and If after subblock is converted.
                    from torch.onnx.symbolic_helper import _onnx_shape_inference
                    if _onnx_shape_inference:
                        torch._C._jit_pass_onnx_node_shape_type_inference(new_node, _params_dict, opset_version)
                    return new_op_outputs
            else:
                symbolic_fn = _find_symbolic_in_registry("prim", op_name, opset_version,
                                                         operator_export_type)
                if symbolic_fn is None:
                    return None
                attrs = {k: n[k] for k in n.attributeNames()}
                # TODO: https://msdata.visualstudio.com/Vienna/_workitems/edit/1408006
                # PythonOp symbolic need access the node to resolve the name conflict,
                # this is inconsistent with regular op symbolic.
                if op_name == "PythonOp":
                    inputs = (n, *inputs)
                return symbolic_fn(g, *inputs, **attrs)

        elif ns == "quantized":
            domain = ""
            if operator_export_type == OperatorExportTypes.ONNX_ATEN_FALLBACK:
                domain = "caffe2"
            symbolic_fn = _find_symbolic_in_registry(domain, op_name, opset_version, operator_export_type)
            if symbolic_fn is None:
                return None
            attrs = {k: n[k] for k in n.attributeNames()}
            return symbolic_fn(g, *inputs, **attrs)

        # custom ops
        elif sym_registry.is_registered_version(ns, opset_version):
            domain = ns
            symbolic_fn = _find_symbolic_in_registry(domain, op_name, opset_version, operator_export_type)
            if symbolic_fn is None:
                return None
            attrs = {k: n[k] for k in n.attributeNames()}
            return symbolic_fn(g, *inputs, **attrs)
        else:
            raise RuntimeError("ONNX export failed on an operator with unrecognized namespace {}::{}. "
                               "If you are trying to export a custom operator, make sure you registered "
                               "it with the right domain and version.".format(ns, op_name))
    except RuntimeError:
        if operator_export_type == OperatorExportTypes.ONNX_FALLTHROUGH:
            return None
        raise
    except TypeError as e:
        # Handle the specific case where we didn't successfully dispatch.
        # Otherwise, the backtrace will have the clues you need.
        e.args = ("{} \n(Occurred when translating {}).".format(e.args[0], op_name),)
        raise
