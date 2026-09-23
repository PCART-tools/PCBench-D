@compatibility(is_backward_compatible=False)
def serialize_module(fx_module: GraphModule, weights: Dict, name_prefix="") -> Dict:
    """Recursively Serializes a graph module (fx_module) to a dictionary which is later exported to JSON.
    It also adds all weights the provided weights dictionary by qualified_name.
    Dictionary Schema:
    MODULE
    {
        modules: {module_name: MODULE],
        nodes: [NODE],
        weights {qualified_name: WEIGHT},
    }
    NODE
    {
        shape: [],
        stride: [],
        dtype: dtype,
        is_quantized: bool,
        target: target,
        op_code: op_code,
        name: name,
        args: [],
        kwargs: {}
    }
    WEIGHT
    {
        dtype: dtype,
        is_quantized: bool,
        shape: [],
        QUANTIZATION,
    }
    QUANTIZATION
    {
        qscheme: qscheme,
        q_scale: float,
        q_zero_point: float,
        q_per_channel_scales, [],
        q_per_channel_zero_points: [],
        q_per_channel_axis, int
    }
    """
    serialized_dict: Dict[str, Any] = {}
    serialized_dict["modules"] = {}
    serialized_dict["weights"] = {}
    serialized_dict["nodes"] = []
    submodules = dict(fx_module.named_modules())
    prefix = f"{name_prefix}." if name_prefix else ""

    def add_weight_tensors(named_tensors):
        for name, p in named_tensors:
            if name.startswith("parent.") or not isinstance(p, torch.Tensor):
                continue
            weight_dict = serialize_weight(p, weights, prefix + name)
            serialized_dict["weights"].update(weight_dict)
            weights[prefix + name] = p

    add_weight_tensors(fx_module.named_parameters())
    add_weight_tensors(fx_module.named_buffers())

    def get_node_info(node):
        tensor_meta = get_tensor_meta(node)
        node_rep = {
            "shape": serialize_shape(tensor_meta.shape),
            "dtype": str(tensor_meta.dtype),
            "requires_grad": str(tensor_meta.requires_grad),
            "stride": serialize_stride(tensor_meta.stride),
            "is_quantized": tensor_meta.is_quantized,
        }

        if tensor_meta.is_quantized:
            node_rep["qscheme"] = str(tensor_meta.qparams["qscheme"])

            if tensor_meta.qparams["qscheme"] in {
                torch.per_tensor_affine,
                torch.per_tensor_symmetric,
            }:
                node_rep["q_scale"] = tensor_meta.qparams["scale"]
                node_rep["q_zero_point"] = tensor_meta.qparams["zero_point"]

        # Add all extra lowering_info that was provided in node.meta.
        lowering_info = node.meta.get("lowering_info")
        if lowering_info is not None:
            overlapping_keys = node_rep.keys() & lowering_info.keys()
            assert (
                len(overlapping_keys) == 0
            ), f"Overlap found between lowering_info and node_rep: {overlapping_keys}"
            node_rep.update(lowering_info)

        return node_rep

    # Note: lift_lowering_attrs_to_nodes is only used to support leaf modules
    # that cannot currently be symbolically traced into, e.g. batch norm.
    lift_lowering_attrs_to_nodes(fx_module)
    for node in fx_module.graph.nodes:
        node_rep: Dict[str, Any] = {}
        # Get shape/type info, currently not needed for call_module node
        # whose target is a GraphModule and output node.
        if (
            not (
                node.op == "call_module"
                and isinstance(submodules[node.target], GraphModule)
            )
            and node.op != "output"
        ):
            node_rep.update(get_node_info(node))

        # Recurse down into any submodules we are calling.
        if node.op == "call_module":
            if isinstance(submodules[node.target], GraphModule):
                serialized_module = serialize_module(
                    getattr(fx_module, node.target), weights, node.target
                )
                serialized_dict["modules"][node.target] = serialized_module
            else:
                node_rep["parameters"] = serialize_leaf_module(
                    node,
                    serialized_dict["weights"],
                    weights,
                    prefix + node.target,
                )

        if node.op == "call_function":
            node_rep["target"] = _get_qualified_name(node.target)
        else:
            node_rep["target"] = str(node.target)

        # Make sure we capture all constants.
        if node.op == "get_attr":
            # If we are targeting a parent constant we update the target.
            if node.target.startswith("parent."):
                stripped_name = node.target[len("parent.") :]
                node.name = stripped_name
                node_rep["target"] = stripped_name
                weight = serialize_weight(
                    weights[stripped_name], weights, node.target[len("parent.") :]
                )
                # For quantized embedding tables we need to update the shape/type,
                # so we check if the users of this get_attr is a quantized EB and this is the weight for the EB.
                user_targets = {
                    _get_qualified_name(n.target)
                    .replace("torch.fx.experimental.fx_acc.", "")
                    .replace("glow.fb.fx.", ""): n
                    for n in node.users.keys()
                }
                if (
                    "acc_ops.embedding_bag_byte_rowwise_offsets" in user_targets
                    and str(
                        user_targets[
                            "acc_ops.embedding_bag_byte_rowwise_offsets"
                        ].kwargs["weight"]
                    )
                    == stripped_name
                ):
                    weight[stripped_name]["dtype"] = "acc.uint8fused"
                # Same as above, but for the 4 bit version.
                if (
                    "acc_ops.embedding_bag_4bit_rowwise_offsets" in user_targets
                    and str(
                        user_targets[
                            "acc_ops.embedding_bag_4bit_rowwise_offsets"
                        ].kwargs["weight"]
                    )
                    == stripped_name
                ):
                    weight[stripped_name]["dtype"] = "acc.uint4fused"

                serialized_dict["weights"].update(weight)
            else:
                # Find the actual target parameter/buffer from the fx_module.
                submod_path, _, target_name = node.target.rpartition(".")
                submod: Optional[torch.nn.Module] = (
                    fx_module.get_submodule(submod_path) if submod_path else fx_module
                )
                assert submod is not None, f"submod {submod_path} not found"
                target = getattr(submod, target_name, None)
                assert target is not None, f"{target_name} not an attr of {submod_path}"
                qualname = prefix + node.target
                # Check that the target is a tensor, and that we haven't added it already from a leaf module.
                if isinstance(target, torch.Tensor) and qualname not in weights:
                    weight = serialize_weight(target, weights, qualname)
                    serialized_dict["weights"].update(weight)
                    weights[qualname] = target

        node_rep["op_code"] = node.op
        node_rep["name"] = node.name

        def get_user_info(user_node: Argument) -> Any:
            return {"is_node": True, "name": str(user_node)}

        def get_arg_info(arg: Argument) -> Any:
            if isinstance(arg, torch.fx.Node):
                return {"is_node": True, "name": str(arg)}
            elif isinstance(arg, (torch.dtype, torch.memory_format, torch.qscheme)):
                return str(arg)
            else:
                return arg

        def get_output_arg_info(arg: Node) -> Dict[str, Any]:
            node_rep: Dict[str, Any] = get_arg_info(arg)
            node_rep.update(get_node_info(arg))
            return node_rep

        if node.op == "output":
            node_rep["args"] = map_arg(
                node.args,
                get_output_arg_info,
            )

            # If there're multiple outputs then node_rep["args"][0] will be a tuple.
            # In this case we want to unpack the tuple.
            if isinstance(node_rep["args"][0], tuple):
                node_rep["args"] = node_rep["args"][0]
        else:
            node_rep["args"] = map_aggregate(node.args, get_arg_info)

        node_rep["kwargs"] = map_aggregate(node.kwargs, get_arg_info)
        node_rep["users"] = map_aggregate(list(node.users.keys()), get_user_info)
        serialized_dict["nodes"] += [node_rep]

    return serialized_dict
