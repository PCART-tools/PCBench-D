def get_opt_ctx(node: torch.fx.Node) -> OptimizationContext:
    return node.meta.get(OptimizationContext.key, None)
