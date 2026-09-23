def prepare_get_standalone_module_configs(
    node: Node,
    modules: Dict[str, torch.nn.Module],
    prepare_custom_config_dict: Dict[str, Any],
    parent_qconfig: QConfigAny,
    parent_backend_config_dict: Optional[Dict[str, Any]],
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """
    Returns the standalone module qconfig_dict and prepare_config_dict
    for `node`, assuming that the module pointed to by `node` is
    a standalone modules.
    """
    standalone_module_name = str(node.target)
    standalone_module_type = type(modules[standalone_module_name])  # type: ignore[index]
    sm_qconfig_dict, sm_prepare_config_dict, sm_backend_config_dict = \
        get_standalone_module_configs(standalone_module_name, standalone_module_type, prepare_custom_config_dict)
    # fallback to use parent module's qconfig if user didn't specify qconfig dict
    if sm_qconfig_dict is None:
        sm_qconfig_dict = {"": parent_qconfig}
    if sm_prepare_config_dict is None:
        sm_prepare_config_dict = {}
    # TODO: sm_backend_config_dict can fallback to use parent's backend_config_dict
    # as well, this can be added later
    if sm_backend_config_dict is None:
        sm_backend_config_dict = parent_backend_config_dict
    return sm_qconfig_dict, sm_prepare_config_dict, sm_backend_config_dict
