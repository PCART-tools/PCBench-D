def fuse_fx(
    model: torch.nn.Module,
    fuse_custom_config: Union[FuseCustomConfig, dict[str, Any], None] = None,
    backend_config: Union[BackendConfig, dict[str, Any], None] = None,
) -> GraphModule:
    r"""Fuse modules like conv+bn, conv+bn+relu etc, model must be in eval mode.
    Fusion rules are defined in torch.ao.quantization.fx.fusion_pattern.py

    Args:

        * `model` (torch.nn.Module): a torch.nn.Module model
        * `fuse_custom_config` (FuseCustomConfig): custom configurations for fuse_fx.
            See :class:`~torch.ao.quantization.fx.custom_config.FuseCustomConfig` for more details
    Example::

        from torch.ao.quantization import fuse_fx
        m = Model().eval()
        m = fuse_fx(m)

    """
    if fuse_custom_config is None:
        fuse_custom_config = FuseCustomConfig()

    if isinstance(fuse_custom_config, dict):
        warnings.warn(
            "Passing a fuse_custom_config_dict to fuse is deprecated and will not be supported "
            "in a future version. Please pass in a FuseCustomConfig instead.",
            FutureWarning,
            stacklevel=2,
        )
        fuse_custom_config = FuseCustomConfig.from_dict(fuse_custom_config)

    torch._C._log_api_usage_once("quantization_api.quantize_fx.fuse_fx")
    preserved_attr_names = fuse_custom_config.preserved_attributes
    preserved_attrs = {
        attr: getattr(model, attr)
        for attr in preserved_attr_names
        if hasattr(model, attr)
    }

    graph_module = torch.fx.symbolic_trace(model)
    _attach_meta_to_node_if_not_exist(graph_module)
    graph_module = _fuse_fx(graph_module, False, fuse_custom_config, backend_config)

    attach_preserved_attrs_to_model(graph_module, preserved_attrs)
    return graph_module
