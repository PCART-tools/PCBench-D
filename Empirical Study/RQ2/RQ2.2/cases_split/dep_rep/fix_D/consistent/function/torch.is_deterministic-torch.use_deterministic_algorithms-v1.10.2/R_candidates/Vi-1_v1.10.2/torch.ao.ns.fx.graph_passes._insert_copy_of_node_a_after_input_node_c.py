def _insert_copy_of_node_a_after_input_node_c(
    input_node_c: Union[Node, List[Node]],
    input_node_c_2: Optional[Union[Node, List[Node]]],
    node_a: Node,
    gm_a: GraphModule,
    gm_b: GraphModule,
    node_name_prefix: str,
) -> Node:
    """
    Assume that node_a from graph_a has
      args (input, (input2)?, arg1, ...), and
      kwargs {kw0: kwarg0, ...}

    Note: input2 is optional. If it equals to None, we assume that the op
    has a single non-param input.  If it is specified, we assume that the op
    has two non-param inputs.

    Copies the underlying values of arg1..argn and kwarg0..kwargn into gm_b,
    and creates the corresponding nodes in graph_c. Note: observers are ignored,
    so if an arg is an observer we navigate up until we find a non-observer parent.

    If node_a is a call_module, points the module pointed to by node_a to gm_b.

    Creates the copy of node_a in graph_c, with input as the first arg,
    and all other args and kwargs pointing to the copies of the objects
    in gm_b created above.

    An example in pictures:

    graph A:
    ========

    input -------------> node_a
                         / / /
    (input_2)?----------/ / /
                         / /
    weight -> weight_obs  /
                         /
    bias ----------------

    graph C (derived from B):
    =========================

    input_node_c --> node_a_copy
                     / / /
    (input_node_c_2)? / /
                     / /
    weight_copy ----/ /
                     /
    bias_copy ------/
    """
    if isinstance(input_node_c, Node):
        graph_c = input_node_c.graph
    else:
        assert isinstance(input_node_c, list)
        graph_c = input_node_c[0].graph

    # generically handle all args and kwargs except for the input
    # Note: this hasn't been tested with many ops, logic may change.
    new_args: List[Any] = []
    # assumes that the first arg is the input
    num_non_param_args = 1 if input_node_c_2 is None else 2
    for node_a_arg in node_a.args[num_non_param_args:]:
        if isinstance(node_a_arg, Node):
            arg_a = return_first_non_observer_node(node_a_arg, gm_a)
            node_a_arg_copy = _copy_node_from_a_to_c(arg_a, gm_a, gm_b, graph_c)
            new_args.append(node_a_arg_copy)
        elif isinstance(node_a_arg, (int, float)):
            new_args.append(node_a_arg)
        elif isinstance(node_a_arg, (list, tuple)):
            for el in node_a_arg:
                assert not isinstance(el, Node), \
                    "handling of Node inside list is not implemented"
            new_args.append(node_a_arg)
        else:
            raise AssertionError(
                f"handling for arg of type {type(node_a_arg)} is not implemented")

    new_kwargs: Dict[str, Any] = {}
    for node_a_k, node_a_kwarg in node_a.kwargs.items():
        if isinstance(node_a_kwarg, Node):
            kwarg_a = return_first_non_observer_node(node_a_kwarg, gm_a)
            node_a_kwarg_copy = _copy_node_from_a_to_c(kwarg_a, gm_a, gm_b, graph_c)
            new_kwargs[node_a_k] = node_a_kwarg_copy
        else:
            new_kwargs[node_a_k] = node_a_kwarg

    node_a_shadows_c_name = \
        get_new_attr_name_with_prefix(node_name_prefix)(gm_b)

    if input_node_c_2:
        input_node_c_args = [input_node_c, input_node_c_2]
    else:
        input_node_c_args = [input_node_c]

    if node_a.op == 'call_module':
        # if target is a module, we point to the module from gm_b
        new_mod_copy_name = \
            get_new_attr_name_with_prefix(node_name_prefix)(gm_b)
        # fetch the corresponding module from gm_a
        assert isinstance(node_a.target, str)
        mod_a = getattr_from_fqn(gm_a, node_a.target)
        setattr(gm_b, new_mod_copy_name, mod_a)
        node_a_shadows_c = graph_c.create_node(
            node_a.op, new_mod_copy_name, (*input_node_c_args, *new_args),
            new_kwargs, node_a_shadows_c_name)
        return node_a_shadows_c
    else:
        assert node_a.op in ('call_function', 'call_method')
        node_a_shadows_c = graph_c.create_node(
            node_a.op, node_a.target, (*input_node_c_args, *new_args),
            new_kwargs, node_a_shadows_c_name)
        return node_a_shadows_c
