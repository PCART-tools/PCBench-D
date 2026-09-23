def maybe_insert_input_observer_for_arg_or_kwarg(
    node: Union[Node, Any],
    arg: Argument,
    qconfig: QConfigAny,
    model: torch.nn.Module,
    modules: Dict[str, torch.nn.Module],
    graph: Graph,
    node_name_to_target_dtype: Dict[str, Dict[str, Optional[torch.dtype]]],
    qhandler: Optional[QuantizeHandler],
    prepare_custom_config_dict: Dict[str, Any],
    backend_config_dict: Optional[Dict[str, Any]],
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
                qhandler,
                prepare_custom_config_dict,
                backend_config_dict)
            new_arg_to_return.append(new_inner_arg)
        return type(arg)(new_arg_to_return)

    if not isinstance(arg, Node):
        return arg
    assert isinstance(arg, Node)
    # default (no observer)
    new_arg = arg

    is_standalone_module = qhandler is not None and \
        isinstance(qhandler, StandaloneModuleQuantizeHandler)
    assert qconfig is not None
    if not is_standalone_module:
        # regular flow for most nodes, except standalone modules
        is_weight = node_arg_is_weight(node, arg)

        is_reuse_input_qconfig_ = is_reuse_input_qconfig(qconfig)

        act_post_process_ctr = qconfig.weight if is_weight else \
            qconfig.activation

        arg_as_output_target_dtype = get_arg_target_dtype_as_output(arg, modules, node_name_to_target_dtype)
        arg_as_input_target_dtype = get_arg_target_dtype_as_input_to_node(arg, node, modules, node_name_to_target_dtype)
        needs_obs = (
            # if the dtypes are different, we need an observer
            (arg_as_output_target_dtype != arg_as_input_target_dtype) and
            # except if the second dtype is float, a dequant will be inserted
            # without an observer in convert
            # TODO(future PR): change this so a placeholder is inserted for
            # future dequants, to make the logic easier to understand
            (arg_as_input_target_dtype != torch.float) and
            # if arg is a bool tensor or not a tensor, do not insert observer
            (arg_as_output_target_dtype not in (torch.bool, None)) and
            # if qconfig is reuse_input qconfig, we won't insert extra observer for input
            not is_reuse_input_qconfig_
        )

    else:
        # custom flow for standalone modules
        _sm_qconfig_dict, sm_prepare_config_dict, _sm_backend_config_dict = \
            prepare_get_standalone_module_configs(
                node, modules, prepare_custom_config_dict, qconfig, backend_config_dict)

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
            arg_as_output_target_dtype = get_arg_target_dtype_as_output(arg, modules, node_name_to_target_dtype)
            arg_as_input_target_dtype = torch.quint8 if cur_input_idx in sm_input_quantized_idxs \
                else torch.float
            needs_obs = (
                (arg_as_output_target_dtype != arg_as_input_target_dtype) and
                (arg_as_input_target_dtype != torch.float)
            )

        act_post_process_ctr = qconfig.activation

    if needs_obs:

        new_obs_mod = act_post_process_ctr()
        existing_obs_node = None

        # Before using the new observer, check if an observer
        # of the correct type already exists. If it does, use it.
        # This prevents duplicate observer insertions if a node is
        # used by multiple nodes.
        # TODO: this is looking into how the value is used in the future
        # we should remove this
        # removing this means we insert one observer for each use, even if they
        # have the same dtype, we can have an extra pass that removes the extra observers
        for maybe_obs_node, _ in arg.users.items():
            if maybe_obs_node.op == 'call_module':
                maybe_obs_mod = modules[maybe_obs_node.target]  # type: ignore[index]
                if (
                    type(maybe_obs_mod) == type(new_obs_mod) and
                    maybe_obs_mod.dtype == arg_as_input_target_dtype
                ):
                    existing_obs_node = maybe_obs_node
                    break

        if existing_obs_node is None:
            new_obs_node = insert_observer(
                arg, node, new_obs_mod, model, modules, graph)
            # override this arg to be the observed arg
            new_arg = new_obs_node
        else:
            new_arg = existing_obs_node

    return new_arg
