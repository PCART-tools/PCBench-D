def warn_if_not_weakly_connected(graph: Graph) -> None:
    """
    Warn the user if the execution graph is not weakly connected.
    """
    if not is_weakly_connected(graph):
        fast_nvcc_warn('execution graph is not (weakly) connected')
