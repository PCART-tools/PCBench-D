def model_is_exported(m: torch.nn.Module) -> bool:
    """
    Return True if the `torch.nn.Module` was exported, False otherwise
    (e.g. if the model was FX symbolically traced or not traced at all).
    """
    return isinstance(m, torch.fx.GraphModule) and any(
        "val" in n.meta for n in m.graph.nodes
    )
