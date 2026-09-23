def straight_line_dependencies(commands: List[str]) -> Graph:
    """
    Return a straight-line dependency graph.
    """
    return [({i - 1} if i > 0 else set()) for i in range(len(commands))]
