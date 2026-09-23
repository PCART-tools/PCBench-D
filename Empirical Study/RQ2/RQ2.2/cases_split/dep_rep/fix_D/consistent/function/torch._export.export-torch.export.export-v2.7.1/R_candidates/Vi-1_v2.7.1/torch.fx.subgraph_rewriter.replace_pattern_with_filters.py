@compatibility(is_backward_compatible=False)
def replace_pattern_with_filters(
    gm: GraphModule,
    pattern: Union[Callable, Graph, GraphModule],
    replacement: Union[Callable, Graph, GraphModule, None] = None,
    match_filters: Optional[
        list[Callable[["InternalMatch", Graph, Graph], bool]]
    ] = None,
    ignore_literals: bool = False,
    # Placed at the end to avoid breaking backward compatibility
    replacement_callback: Optional[
        Callable[["InternalMatch", Graph, Graph], Graph]
    ] = None,
) -> list[ReplacedPatterns]:
    """
    See replace_pattern for documentation. This function is an overload with an additional match_filter argument.

    Args:
        ``match_filters``: A list of functions that take in
            (match: InternalMatch, original_graph: Graph, pattern_graph: Graph) and return a boolean indicating
            whether the match satisfies the condition.
            See matcher_utils.py for definition of InternalMatch.
        ``replacement_callback``: A function that takes in a match and returns a
            Graph to be used as the replacement. This allows you to construct a
            replacement graph based on the match.
    """

    return _replace_pattern(
        gm, pattern, replacement, match_filters, ignore_literals, replacement_callback
    )
