def insert_type_promotion_nodes(
    graph_module: torch.fx.GraphModule,
) -> None:
    """Inplace pass to insert explicit type promotion nodes, recursively through nested modules."""
    for module in graph_module.modules():
        assert isinstance(module, torch.fx.GraphModule)
        passes.InsertTypePromotion(module).run()
