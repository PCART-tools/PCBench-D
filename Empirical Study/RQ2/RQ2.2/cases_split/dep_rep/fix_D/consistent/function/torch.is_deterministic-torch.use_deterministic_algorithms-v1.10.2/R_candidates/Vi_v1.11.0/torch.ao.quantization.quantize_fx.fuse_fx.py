def fuse_fx(
    model: torch.nn.Module, fuse_custom_config_dict: Optional[Dict[str, Any]] = None
) -> GraphModule:
    r""" Fuse modules like conv+bn, conv+bn+relu etc, model must be in eval mode.
    Fusion rules are defined in torch.quantization.fx.fusion_pattern.py

    Args:

        * `model`: a torch.nn.Module model
        * `fuse_custom_config_dict`: Dictionary for custom configurations for fuse_fx, e.g.::

            fuse_custom_config_dict = {
              "additional_fuser_method_mapping": {
                (Module1, Module2): fuse_module1_module2
              }

              # Attributes that are not used in forward function will
              # be removed when constructing GraphModule, this is a list of attributes
              # to preserve as an attribute of the GraphModule even when they are
              # not used in the code, these attributes will also persist through deepcopy
              "preserved_attributes": ["preserved_attr"],
            }

    Example::

        from torch.ao.quantization import fuse_fx
        m = Model().eval()
        m = fuse_fx(m)

    """
    torch._C._log_api_usage_once("quantization_api.quantize_fx.fuse_fx")
    assert not model.training, "fuse_fx only works on models in eval mode"
    check_is_valid_fuse_custom_config_dict(fuse_custom_config_dict)
    graph_module = torch.fx.symbolic_trace(model)
    preserved_attributes: Set[str] = set()
    if fuse_custom_config_dict:
        preserved_attributes = set(
            fuse_custom_config_dict.get("preserved_attributes", [])
        )
    for attr_name in preserved_attributes:
        setattr(graph_module, attr_name, getattr(model, attr_name))
    return _fuse_fx(graph_module, False, fuse_custom_config_dict)
