def insert_observers_for_model(
    model: GraphModule,
    modules: Dict[str, torch.nn.Module],
    matches: Dict[str, MatchResult],
    qconfig_map: Dict[str, QConfigAny],
    graph: Graph,
    prepare_custom_config_dict: Dict[str, Any],
    equalization_config_map: Dict[str, Any],
    input_quantized_idxs: List[int],
    output_quantized_idxs: List[int],
) -> Optional[Node]:
    """
    Inserts observers, using the following high level algorithm:

    For each node in the graph:
      1. determine the target dtype of this node in the quantized graph, and save
           it for future steps
      2. determine the target dtype or all args and kwargs of this node
      3. if any arg or kwarg's target dtype does not match the current node's
           dtype, insert an observer
      4. if the current node needs an output observer, insert it

    For example:

    - starting graph:
        x0 -> linear -> x1

    - observed graph after processing x0:
        x0(fp32)

    - observed graph after processing linear:
        x0(fp32) -> x0_obs0(int8) -> linear(int8) -> linear_obs0(int8)

    - observed graph after processing x1:
        x0(fp32) -> x0_obs0(int8) -> linear(int8) -> linear_obs0(int8) -> x1

    After a node is processed, the naive observer placement is guaranteed to be
    complete for that node and all of its predecessors. There can be future
    passes which optimize the graph by deduplicating observers, etc.
    """

    node_name_to_target_dtype: Dict[str, Any] = {}
    cache_for_no_tensor_check: Dict[Node, bool] = dict()

    inputs_seen_counter = 0
    outputs_seen_counter = 0
    results_node = None

    # first, populate the dtype map based only on qconfig and qhandler
    # this assumes:
    # graph inputs are fp32 by default, and int8 where overriden
    # other nodes output dtype is specified by the qconfig
    modules = dict(model.named_modules(remove_duplicate=False))
    for node in model.graph.nodes:
        root_node, matched_nodes, pattern, qhandler, qconfig = matches.get(
            node.name, (None, None, None, None, None))
        node_name_to_target_dtype[node.name] = get_target_activation_dtype_for_node(
            node, qconfig, inputs_seen_counter, outputs_seen_counter,
            input_quantized_idxs, output_quantized_idxs, qhandler,
            modules, cache_for_no_tensor_check)

    # Second, for nodes with known input dtypes, propagate them throughout the
    # graph. For example, if there is a call such as
    #   x1 = x0.masked_fill(mask, 1)
    # we propagate the type of mask to be torch.bool
    propagate_dtypes_for_known_nodes(
        model.graph, node_name_to_target_dtype, matches)

    # After this point, the current node and all of its arguments
    # have a dtype assigned. Now, we insert observers for inputs
    # of this node (if needed for this node), and the output of this node
    # (if needed for this node).

    # Since we are mutating the graph as we go, we iterate over the original
    # nodes before observer insertion, instead of model.graph.nodes.
    nodes_before_observation = list(model.graph.nodes)

    for node in nodes_before_observation:

        if node.op == 'placeholder':
            # if a graph input is in fp32, it does not need observation
            # if a graph input is in int8, we assume the observation happens
            #   outside of the graph, and no additional observation is needed
            pass

        elif node.op in ('call_module', 'call_method', 'call_function', 'output'):
            # check for matches
            root_node, matched_nodes, pattern, qhandler, qconfig = matches.get(
                node.name, (None, None, None, None, None))
            equalization_qconfig = equalization_config_map.get(node.name, None)

            this_node_dtype = node_name_to_target_dtype[node.name]
            output_not_a_tensor = this_node_dtype is None
            # TODO(future PR): consider stopping matching getitem
            is_getitem = node.op == 'call_function' and \
                node.target == operator.getitem

            skip_inserting_observers = (
                (qconfig is None) or
                output_not_a_tensor or
                is_getitem
            ) and (not node.op == 'output')

            if not skip_inserting_observers:
                modules = dict(model.named_modules(remove_duplicate=False))
                if node.op != 'output':

                    # This is currently only used for equalization.
                    # Checks if the current node is in a branch in which the two
                    # first layers are both being quantized.
                    #
                    # ex.       conv2
                    #         /
                    #      x -> conv1
                    #
                    # If this is the case, we will not apply equalization to the
                    # initial two layers.
                    is_quantized_branch = False
                    if (
                        len(node.args) > 0 and
                        isinstance(node.args[0], Node) and
                        len(node.args[0].users) > 1
                    ):
                        for user in node.args[0].users:
                            # Checks if there exists another user being quantized
                            is_user_quantized = (
                                qconfig_map.get(user.name, None) is not None or
                                (user.op == 'call_module' and isinstance(modules[str(user.target)], ObserverBase))
                            )
                            if user != node and is_user_quantized:
                                is_quantized_branch = True

                    # this modifies node inplace
                    maybe_insert_input_observers_for_node(
                        node, qconfig, model, modules, graph,
                        node_name_to_target_dtype,
                        qhandler, prepare_custom_config_dict)

                    # Insert equalization input observers if needed
                    maybe_insert_input_equalization_observers_for_node(
                        node, equalization_qconfig, model, modules, graph,
                        node_name_to_target_dtype, is_quantized_branch)

                    is_last_node_of_pattern = root_node is node
                    is_general_tensor_value_op = \
                        (qhandler is not None and qhandler.is_general_tensor_value_op())

                    is_general_tensor_shape_op = \
                        (qhandler is not None and qhandler.is_general_tensor_shape_op())

                    if is_last_node_of_pattern and not is_general_tensor_shape_op:
                        # this returns the new observer node if it was needed
                        maybe_output_obs_node = maybe_insert_output_observer_for_node(
                            node, model, modules, graph, matches,
                            node_name_to_target_dtype, pattern, qhandler)
                        if maybe_output_obs_node is not None:
                            # Update users of original node to use the output observer
                            # instead. For example, change
                            #
                            #           next_node
                            #          /
                            #   cur_node -> obs
                            #
                            # to
                            #
                            #                 next_node
                            #                 /
                            #   cur_node -> obs
                            #
                            # We need to save orig users before updating uses because
                            # the list of users will change as we update uses
                            orig_users = list(node.users.keys())
                            for user_node in orig_users:
                                if user_node is maybe_output_obs_node:
                                    continue
                                user_node.replace_input_with(node, maybe_output_obs_node)

                            # for general tensor value ops, we modify the graph
                            # to make all inputs and outputs use the first input's
                            # observer
                            if is_general_tensor_value_op:
                                if not maybe_make_input_output_share_observers(node, model, modules):
                                    remove_output_observer(node, model, modules)

                            if isinstance(qhandler, CustomModuleQuantizeHandler):
                                swap_custom_module_to_observed(node, qconfig, modules, prepare_custom_config_dict)

                else:  # output
                    maybe_insert_observers_before_graph_output(
                        node, output_quantized_idxs,
                        node_name_to_target_dtype, qconfig_map,
                        model, modules, graph)

        #
        # After this point, the current node has input and output observers
        # that it needs for itself inserted.
        #

        # increment the counters, so future inputs and outputs are assigned
        # correct dtypes
        if node.op == 'placeholder':
            inputs_seen_counter += 1
        elif node.op == 'output':
            outputs_seen_counter += 1
            results_node = node

    return results_node
