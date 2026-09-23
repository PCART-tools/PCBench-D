def get_node_first_input_and_output_type(
    node: Node,
    gm: GraphModule,
    logger_cls: Callable,
    node_type_to_io_type_map: Dict[str, Set[NSNodeTargetType]],
) -> Tuple[NodeInputOrOutputType, NodeInputOrOutputType]:

    # TODO(future PR): clean this up
    FUNS_IO_TYPE_FP32 = node_type_to_io_type_map["funs_io_type_fp32"]
    FUNS_IO_TYPE_FP16 = node_type_to_io_type_map["funs_io_type_fp16"]
    FUNS_IO_TYPE_INT8 = node_type_to_io_type_map["funs_io_type_int8"]
    FUNS_IO_TYPE_FP32_OR_INT8 = node_type_to_io_type_map["funs_io_type_fp32_or_int8"]
    MODS_IO_TYPE_FP32 = node_type_to_io_type_map["mods_io_type_fp32"]
    MODS_IO_TYPE_INT8 = node_type_to_io_type_map["mods_io_type_int8"]
    MODS_IO_TYPE_FP32_OR_INT8 = node_type_to_io_type_map["mods_io_type_fp32_or_int8"]
    METHS_IO_TYPE_FP32_OR_INT8 = node_type_to_io_type_map["meths_io_type_fp32_or_int8"]

    if node.op == "call_function":
        if node.target in FUNS_IO_TYPE_FP32:
            return (NodeInputOrOutputType.FP32, NodeInputOrOutputType.FP32)
        if node.target in FUNS_IO_TYPE_FP16:
            return (NodeInputOrOutputType.FP16, NodeInputOrOutputType.FP16)
        elif node.target in FUNS_IO_TYPE_INT8:
            return (NodeInputOrOutputType.INT8, NodeInputOrOutputType.INT8)
        elif node.target in FUNS_IO_TYPE_FP32_OR_INT8:
            return (
                NodeInputOrOutputType.FP32_OR_INT8,
                NodeInputOrOutputType.FP32_OR_INT8,
            )
        else:
            return (NodeInputOrOutputType.UNKNOWN, NodeInputOrOutputType.UNKNOWN)

    elif node.op == "call_module":
        assert node.op == "call_module"
        assert isinstance(node.target, str)
        mod = getattr_from_fqn(gm, node.target)
        if isinstance(mod, (logger_cls, ObserverBase, FakeQuantizeBase)):  # type: ignore[arg-type]
            # A logger or observer's input and output type is the output
            # type of the preceding node.
            first_arg = node.args[0]
            assert isinstance(first_arg, Node)
            (
                _prev_node_input_type,
                prev_node_output_type,
            ) = get_node_first_input_and_output_type(
                first_arg, gm, logger_cls, node_type_to_io_type_map
            )
            return (prev_node_output_type, prev_node_output_type)
        is_known_fp32_input_module = any(
            isinstance(mod, target_type) for target_type in MODS_IO_TYPE_FP32  # type: ignore[arg-type]
        )
        is_known_int8_input_module = any(
            isinstance(mod, target_type) for target_type in MODS_IO_TYPE_INT8  # type: ignore[arg-type]
        )
        is_known_fp32_or_int8_input_module = any(
            isinstance(mod, target_type) for target_type in MODS_IO_TYPE_FP32_OR_INT8  # type: ignore[arg-type]
        )
        if is_known_fp32_input_module:
            return (NodeInputOrOutputType.FP32, NodeInputOrOutputType.FP32)
        elif is_known_int8_input_module:
            return (NodeInputOrOutputType.INT8, NodeInputOrOutputType.INT8)
        elif is_known_fp32_or_int8_input_module:
            return (
                NodeInputOrOutputType.FP32_OR_INT8,
                NodeInputOrOutputType.FP32_OR_INT8,
            )
        else:
            return (NodeInputOrOutputType.UNKNOWN, NodeInputOrOutputType.UNKNOWN)

    elif node.op == "call_method":
        if node.target == "dequantize":
            # Dequantize is a special node because it allows multiple input types.
            # So, we look up the output type of the previous node and return that
            # as the input type of this node instance.
            prev_node = node.args[0]
            assert isinstance(prev_node, Node)
            (
                _prev_node_input_type,
                prev_node_output_type,
            ) = get_node_first_input_and_output_type(
                prev_node, gm, logger_cls, node_type_to_io_type_map
            )
            return (prev_node_output_type, NodeInputOrOutputType.FP32)

        elif node.target == "to":
            # to is a special node because it allows multiple input types.
            # So, we look up the output type of the previous node and return that
            # as the input type of this node instance. We also look up the target
            # of to and return the correct output type.
            prev_node = node.args[0]
            assert isinstance(prev_node, Node)
            (
                _prev_node_input_type,
                prev_node_output_type,
            ) = get_node_first_input_and_output_type(
                prev_node, gm, logger_cls, node_type_to_io_type_map
            )

            cur_node_dtype_target = node.args[1]
            assert (
                cur_node_dtype_target is torch.float16
            ), f"{cur_node_dtype_target} handling needs to be added"

            return (prev_node_output_type, NodeInputOrOutputType.FP16)

        elif node.target in METHS_IO_TYPE_FP32_OR_INT8:
            return (
                NodeInputOrOutputType.FP32_OR_INT8,
                NodeInputOrOutputType.FP32_OR_INT8,
            )

        return (NodeInputOrOutputType.UNKNOWN, NodeInputOrOutputType.UNKNOWN)
    else:
        return (NodeInputOrOutputType.UNKNOWN, NodeInputOrOutputType.UNKNOWN)
