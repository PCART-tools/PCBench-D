def _check_valid_autocast_block(
    enter_autocast_node: torch.fx.Node, exit_autocast_node: torch.fx.Node
) -> None:
    assert _is_enter_autocast_node(enter_autocast_node)
    assert _is_exit_autocast_node(exit_autocast_node)
    assert exit_autocast_node.args[0] == enter_autocast_node
