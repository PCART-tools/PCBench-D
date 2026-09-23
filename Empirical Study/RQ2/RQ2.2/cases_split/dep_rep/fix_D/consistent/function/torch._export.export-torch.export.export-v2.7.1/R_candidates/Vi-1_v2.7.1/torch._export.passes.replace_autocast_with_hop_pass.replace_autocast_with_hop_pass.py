def replace_autocast_with_hop_pass(
    gm: torch.fx.GraphModule, graph_signature: Optional[ExportGraphSignature]
) -> tuple[torch.fx.GraphModule, Optional[ExportGraphSignature]]:
    """
    Split gm into sub-graph-modules using `sequential_split_and_maybe_inline_subgraphs`, and
    then recursively call itself on each of the submodules.
    """
    return _replace_with_hop_pass_helper(
        gm,
        graph_signature,
        _sequential_split_and_maybe_inline_subgraphs,
    )
