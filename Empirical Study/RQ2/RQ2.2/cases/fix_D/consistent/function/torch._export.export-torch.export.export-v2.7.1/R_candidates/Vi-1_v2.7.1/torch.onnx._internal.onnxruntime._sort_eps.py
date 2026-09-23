def _sort_eps(eps: tuple[str, ...]) -> tuple[str, ...]:
    """Sort execution providers in eps based on pre-set priority."""

    def get_execution_provider_priority(ep: str) -> int:
        if ep == "CPUExecutionProvider":
            # Lowest priority.
            return 2
        if ep == "CUDAExecutionProvider":
            # Higher priority than CPU but lower than
            # other specialized EPs.
            return 1
        # Highest priority.
        return 0

    unique_eps = set(eps)
    return tuple(sorted(unique_eps, key=get_execution_provider_priority, reverse=True))
