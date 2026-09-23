def _replace_with_hop_pass_helper(
    gm: torch.fx.GraphModule,
    graph_signature: Optional[ExportGraphSignature],
    sequential_split_and_maybe_inline_subgraphs: Callable[
        [torch.fx.GraphModule, Optional[ExportGraphSignature]],
        tuple[torch.fx.GraphModule, Optional[ExportGraphSignature]],
    ],
) -> tuple[torch.fx.GraphModule, Optional[ExportGraphSignature]]:
    """
    Split gm into sub-graph-modules using `sequential_split_and_maybe_inline_subgraphs`, and
    then recursively call itself on each of the submodules.
    """
    new_gm, new_signature = sequential_split_and_maybe_inline_subgraphs(
        gm, graph_signature
    )
    # recursively call
    for node in new_gm.graph.nodes:
        if node.op == "get_attr":
            subgm = getattr(new_gm, node.target)
            if not isinstance(subgm, torch.fx.GraphModule):
                continue
            new_subgm, _ = _replace_with_hop_pass_helper(
                subgm,
                None,
                sequential_split_and_maybe_inline_subgraphs,
            )
            setattr(new_gm, node.target, new_subgm)

    new_gm.recompile()
    new_gm.graph.lint()
    return new_gm, new_signature
