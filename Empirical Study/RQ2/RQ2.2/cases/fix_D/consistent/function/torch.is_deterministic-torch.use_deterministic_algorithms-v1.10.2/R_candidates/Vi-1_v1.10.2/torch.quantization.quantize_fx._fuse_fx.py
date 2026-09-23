def _fuse_fx(
        graph_module: GraphModule,
        fuse_custom_config_dict: Dict[str, Any] = None) -> GraphModule:
    r""" Internal helper function to fuse modules in preparation for quantization

    Args:
        graph_module: GraphModule object from symbolic tracing (torch.fx.symbolic_trace)
    """
    _check_is_graph_module(graph_module)
    fuser = Fuser()
    return fuser.fuse(graph_module, fuse_custom_config_dict)
