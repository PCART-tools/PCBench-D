def is_leaf(
    m: torch.nn.Module,
    prepare_custom_config_dict: Optional[Dict[str, Any]],
) -> bool:
    if prepare_custom_config_dict is None:
        prepare_custom_config_dict = {}

    if 'non_traceable_module_class' in prepare_custom_config_dict:
        for target_cls in prepare_custom_config_dict['non_traceable_module_class']:
            if isinstance(m, target_cls):
                return True

    # TODO(future PR): extend to the rest of the container classes
    container_classes = (
        torch.nn.Sequential,
        torch.nn.ModuleList,
    )
    return (
        # allowlist everything in torch.nn except containers
        (m.__module__.startswith('torch.nn') and (
            not isinstance(m, container_classes)
        )) or
        # allowlist nni modules, as they inherit from nn.Sequential
        m.__module__.startswith('torch.nn.intrinsic') or
        # observers and fake quants are leaves
        is_activation_post_process(m)
    )
