def _ensure_proper_output_use(user: fx.Node, target_node: fx.Node) -> int:
    """
    Ensures the node looks in proper form of calling the output of an fx2trt
    splitter sub-net. Specifically:

    1. op is call function, target: operator.getitem
    2. args is a 2-element tuple
    3. args[0] is the name of the subnet's output
    4. args[1] is the index into the subnet output tuple

    E.g.:

        %getitem_4 : [#users=1] = call_function[target=operator.getitem](args = (%_run_on_acc_1, 4), kwargs = {})

    returns the index into the subnet output tuple
    """
    _LOGGER.info(f"Checking user node: {user.format_node()}")
    assert (
        user.op == "call_function"
        and user.target == operator.getitem
        and len(user.args) == 2
        and isinstance(user.args[0], fx.Node)
        and user.args[0].name == target_node.name
        and isinstance(user.args[1], int)
    ), f"Node is not a proper user of splitter output: {user.format_node()}"

    return user.args[1]
