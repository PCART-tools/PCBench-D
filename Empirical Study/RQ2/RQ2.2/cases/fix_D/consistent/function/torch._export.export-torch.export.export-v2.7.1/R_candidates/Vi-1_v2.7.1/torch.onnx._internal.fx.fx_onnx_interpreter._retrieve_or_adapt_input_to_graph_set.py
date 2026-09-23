def _retrieve_or_adapt_input_to_graph_set(
    fx_node_arg: fx_type_utils.Argument,
    fx_name_to_onnxscript_value: dict[
        str,
        onnxscript_graph_building.TorchScriptTensor
        | tuple[onnxscript_graph_building.TorchScriptTensor, ...],
    ],
    tracer: onnxscript_graph_building.TorchScriptTracingEvaluator,
):
    """Map FX value to TorchScript value.

    When creating TorchScript graph from FX graph, we need a mapping from FX variable
    to TorchScript variable. This function maps FX variable, fx_node_arg, to torch.jit.Value.
    """
    from onnxscript import opset18 as op

    onnx_tensor = fx_node_arg
    if isinstance(onnx_tensor, torch.fx.Node):
        # 1. fx_node_arg is a torch.fx.Node, which means
        #    fx_node_arg stands for the output of that torch.fx.Node.
        # 2. fx_node_arg (variable in torch.fx.Graph) is be mapped to
        #    torch.jit.Value, fx_name_to_onnxscript_value[fx_node_arg.name],
        #    in TorchScript graph.
        return fx_name_to_onnxscript_value[onnx_tensor.name]
    elif isinstance(onnx_tensor, (tuple, list)) and any(
        isinstance(node, torch.fx.Node)
        and fx_type_utils.is_torch_symbolic_type(node.meta.get("val"))
        for node in onnx_tensor
    ):
        # This intends to handle dynamic axes. for example, if the input size of op.Expand
        # is dynamic, each dimension would be variable (i.e., sym variable in Pytorch
        # FX graph. Note that sym variable is mapped to tensor in ONNX Script world)
        # calculated by other operators.
        sequence_mixed_elements: list[
            onnxscript_graph_building.TorchScriptTensor
            | tuple[onnxscript_graph_building.TorchScriptTensor, ...]
            | list[int]
        ] = []
        # onnx_tensor contains a list of scalars which could be one of
        #   - tensor with empty shape,
        #   - tensor with tensor with shape (1,),
        #   - torch.SymInt,
        #   - int
        #   - ...
        # They should all be promoted to tensor with shape (1,)
        # in order to call ONNX's Concat.
        for tensor in onnx_tensor:
            # Prepare `tensor` as input of ONNX's Concat.

            if isinstance(
                tensor, torch.fx.Node
            ) and fx_type_utils.is_torch_symbolic_type(tensor.meta.get("val")):
                # In this case, tensor is a torch.SymInt from Dynamo's perspective.
                # It might be mapped to tensor with shape () or (1,) in ONNX.
                element_value = fx_name_to_onnxscript_value[tensor.name]
                if isinstance(
                    element_value, onnxscript_graph_building.TorchScriptTensor
                ):
                    # All elements sequence_mixed_elements will be send to onnx's Concat
                    # as inputs. Therefore, they are required to have the same rank.
                    # Since tensors with rank=0 (i.e., scalar) cannot be concated, all
                    # scalars are promoted to tensors with shape (1,).
                    with onnxscript.evaluator.default_as(tracer):
                        element_value = op.Reshape(
                            element_value,  # type: ignore[arg-type, type-var]
                            [1],  # type: ignore[arg-type, type-var]
                        )
                sequence_mixed_elements.append(element_value)
            elif isinstance(tensor, int):
                # NOTE: op.Concat doesn't support scalar, so we need to wrap it with
                # dim, and onnx-script will promote it to tensor(int64)
                sequence_mixed_elements.append([tensor])
            else:
                raise RuntimeError(
                    f"Unsupported type in sequence_mixed_elements: {type(tensor)}"
                )
        # Concat all the elements in the sequence.
        # shapes are mapped to tensors in ONNX graph (TorchScriptGraph),
        # so list of sym_ints is concatenated to a tensor before calling ONNX op.

        # For example:
        #    inputs: [[2], [4], fx.Node(SymIntA), [1], fx.Node(SymIntB)]
        #    outputs: op.Concat([op.Constant(2), op.Constant(4), TorchScriptTensor(A), op.Constant(1), TorchScriptTensor(B)])

        # onnx-script auto wraps python number with op.Constants,
        # so we don't need to specifically process them.
        with onnxscript.evaluator.default_as(tracer):
            output = op.Concat(*sequence_mixed_elements, axis=0)  # type: ignore[type-var]
        output.dtype = torch.int64  # type: ignore[union-attr]
        output.shape = [len(sequence_mixed_elements)]  # type: ignore[union-attr]
        return output
    elif isinstance(onnx_tensor, (tuple, list)) and all(
        isinstance(node, torch.fx.Node) or node is None for node in onnx_tensor
    ):
        sequence_elements: list[
            onnxscript_graph_building.TorchScriptTensor
            | None
            | tuple[onnxscript_graph_building.TorchScriptTensor, ...]
        ] = []
        for tensor in onnx_tensor:
            sequence_elements.append(
                fx_name_to_onnxscript_value[tensor.name] if tensor is not None else None  # type: ignore[index, union-attr]
            )
        return sequence_elements
    if isinstance(onnx_tensor, torch.dtype):
        onnx_tensor = int(  # type: ignore[call-overload]
            jit_type_utils.JitScalarType.from_dtype(onnx_tensor).onnx_type()
        )
    # NOTE: if device is specified in kwargs (not consumed), it's free to ignored. But
    # if it's in args, we need to set it to string for dispatcher to match schema.
    if isinstance(onnx_tensor, torch.device):
        # torch.device is not supported by onnxscript (no op). We turn it into
        # a string.
        return str(onnx_tensor)
    # all other cases, we do nothing.
    return onnx_tensor
