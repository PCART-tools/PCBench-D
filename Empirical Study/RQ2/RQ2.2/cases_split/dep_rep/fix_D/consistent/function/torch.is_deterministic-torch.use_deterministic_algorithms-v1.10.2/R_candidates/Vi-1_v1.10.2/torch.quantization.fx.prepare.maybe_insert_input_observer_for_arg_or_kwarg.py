def maybe_insert_input_observer_for_arg_or_kwarg(
    node: Union[Node, Any],
    arg: Argument,
    qconfig: QConfigAny,
    model: torch.nn.Module,
    modules: Dict[str, torch.nn.Module],
    graph: Graph,
    node_name_to_target_dtype: Dict[str, Any],
    qhandler: Optional[QuantizeHandler],
    prepare_custom_config_dict: Dict[str, Any],
) -> Argument:
    """
    Given a `node` and an `arg`, inserts an input observer between
    `node` and `arg` if necessary.
    """
    # for ops such as torch.cat([x0, x1]),
    # traverse through the list
    if isinstance(arg, (list, tuple)):
        new_arg_to_return = []
        for inner_arg in arg:
            new_inner_arg = maybe_insert_input_observer_for_arg_or_kwarg(
                node, inner_arg, qconfig, model, modules,
                graph, node_name_to_target_dtype,
                qhandler, prepare_custom_config_dict)
            new_arg_to_return.append(new_inner_arg)
        return type(arg)(new_arg_to_return)

    if not isinstance(arg, Node):
        return arg
    assert isinstance(arg, Node)

    # default (no observer)
    new_arg = arg

    is_standalone_module = qhandler is not None and \
        isinstance(qhandler, StandaloneModuleQuantizeHandler)

    if not is_standalone_module:
        # regular flow for most nodes, except standalone modules
        is_weight = node_arg_is_weight(node, arg)
        assert qconfig is not None

        act_post_process_ctr = qconfig.weight if is_weight else \
            qconfig.activation

        is_bias = node_arg_is_bias(node, arg)
        is_activation = not (is_weight or is_bias)
        weight_needs_obs = is_weight and weight_is_quantized(qconfig) and node.target not in NON_QUANTIZABLE_WEIGHT_OPS
        bias_needs_obs = \
            (is_bias and activation_dtype(qconfig) == torch.float16) and \
            weight_dtype(qconfig) == torch.float16

        arg_dtype = node_name_to_target_dtype[arg.name]
        node_dtype = node_name_to_target_dtype[node.name]
        dtype_changes_and_second_dtype_not_float = (
            # if the dtypes are different, we need an observer
            (arg_dtype != node_dtype) and
            # except if the second dtype is float, a dequant will be inserted
            # without an observer in convert
            # TODO(future PR): change this so a placeholder is inserted for
            # future dequants, to make the logic easier to understand
            (node_dtype != torch.float) and
            # if arg is a bool tensor or not a tensor, do not insert observer
            (arg_dtype not in (torch.bool, None)) and
            (is_activation and activation_is_statically_quantized(qconfig))
        )

        needs_obs = (
            weight_needs_obs or
            bias_needs_obs or
            dtype_changes_and_second_dtype_not_float
        )

    else:
        # custom flow for standalone modules
        _sm_qconfig_dict, sm_prepare_config_dict = \
            get_standalone_module_configs(
                node, modules, prepare_custom_config_dict, qconfig)

        sm_input_quantized_idxs = \
            sm_prepare_config_dict.get('input_quantized_idxs', [])
        # for args, this is set to the index of the current arg
        # for kwargs, this is left at None
        cur_input_idx = None
        for arg_idx, arg_to_check in enumerate(node.args):
            if arg_to_check is arg:
                cur_input_idx = arg_idx
                break

        if cur_input_idx is None:
            needs_obs = False
        else:
            arg_dtype = node_name_to_target_dtype[arg.name]
            node_dtype = torch.quint8 if cur_input_idx in sm_input_quantized_idxs \
                else torch.float
            needs_obs = (
                (arg_dtype != node_dtype) and
                (node_dtype != torch.float)
            )

    if needs_obs:

        new_obs_mod = act_post_process_ctr()
        existing_obs_node = None

        # Before using the new observer, check if an observer
        # of the correct type already exists. If it does, use it.
        # This prevents duplicate observer insertions if a node is
        # used by multiple nodes.
        for maybe_obs_node, _ in arg.users.items():
            if maybe_obs_node.op == 'call_module':
                maybe_obs_mod = modules[maybe_obs_node.target]  # type: ignore[index]
                if (
                    type(maybe_obs_mod) == type(new_obs_mod) and
                    node_name_to_target_dtype[maybe_obs_node.name] == node_dtype
                ):
                    existing_obs_node = maybe_obs_node
                    break

        if existing_obs_node is None:
            new_obs_node = insert_observer(
                arg, new_obs_mod, model, modules, graph)
            # set the type, so the next node can read it
            node_name_to_target_dtype[new_obs_node.name] = node_dtype
            # override this arg to be the observed arg
            new_arg = new_obs_node
        else:
            new_arg = existing_obs_node

    return new_arg
