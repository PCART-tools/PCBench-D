def _find_matches(
    root: GraphModule,
    graph: Graph,
    pattern_to_fuse_handler_cls: dict[Pattern, Callable],
) -> dict[str, tuple[Node, Pattern, NodePattern, FuseHandler, dict[Node, Any]]]:
    modules = dict(root.named_modules())
    # node name -> (root_node, match_value)
    match_map: dict[
        str, tuple[Node, Pattern, NodePattern, FuseHandler, dict[Node, Any]]
    ] = {}
    # a map from node to the matched subpattern
    node_to_subpattern: dict[Node, Any] = {}

    # TODO: dedup with quantization matching function in match_utils.py
    def apply_match(pattern, node, match, matched_node_pattern, node_to_subpattern):
        if isinstance(pattern, tuple):
            s, *args = pattern
            current_node_pattern: list[Node] = []
            apply_match(s, node, match, current_node_pattern, node_to_subpattern)
            for subpattern, arg in zip(args, node.args):
                apply_match(
                    subpattern, arg, match, current_node_pattern, node_to_subpattern
                )
            matched_node_pattern.append(tuple(current_node_pattern))
        else:
            # the first pattern matches will take precedence
            if node.name not in match_map:
                matched_node_pattern.append(node)
                # MatchAllNode here is actually MatchAllInputNode which should not
                # be added to match_map
                if pattern is not MatchAllNode:
                    node_to_subpattern[node] = pattern
                    root_node, pattern, handler = match
                    match_map[node.name] = (
                        root_node,
                        pattern,
                        matched_node_pattern,
                        handler,
                        node_to_subpattern,
                    )

    for node in reversed(graph.nodes):
        if node.name not in match_map:
            for pattern, fuse_handler_cls in pattern_to_fuse_handler_cls.items():
                matched_node_pattern: list[Node] = []
                if _is_match(modules, node, pattern):
                    apply_match(
                        pattern,
                        node,
                        (node, pattern, fuse_handler_cls(node)),
                        matched_node_pattern,
                        node_to_subpattern,
                    )
                    break

    return match_map
