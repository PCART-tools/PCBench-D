    def _get_remaining_users(extra_input_node, compute_node):
        # Think about this pattern:
        #      ReLU
        #     /   \
        #  Conv1
        #   /      \
        # Conv2
        #   \      /
        #      Add
        # Although, the extra input node (ReLU) has more than 1 users: Conv1 and Add.
        # The Conv1 is the ancestor node of the current compute node (Conv2).
        # This indicates that the buffer of ReLU has completed all its usage,
        # So we can safely make changes to it now by doing Conv2->Add inplace fusion.
        # Take above case as example:
        # * extra_input_node: ReLU
        # * compute_node: Conv2
        # _get_remaining_users will return the users of extra_input_node which are not
        # ancestor node of compute_node.
        def _is_ancestor_node(_current_node, _ancestor_node):
            # Check whether _ancestor_node is the ancestor node of _current_node
            _node_list = [_current_node]
            _visited_nodes = OrderedSet[torch.fx.Node]()
            while len(_node_list) != 0:
                _current_node = _node_list.pop(0)
                if _current_node not in _visited_nodes:
                    _visited_nodes.add(_current_node)
                    if _current_node == _ancestor_node:
                        return True
                    elif isinstance(
                        _current_node, torch.fx.Node
                    ) and _current_node.op not in ["placeholder", "output", "get_attr"]:
                        for input in _current_node.all_input_nodes:
                            _node_list.append(input)  # noqa: PERF402
            return False

        return [
            user
            for user in list(extra_input_node.users)
            if not _is_ancestor_node(compute_node, user)
        ]
