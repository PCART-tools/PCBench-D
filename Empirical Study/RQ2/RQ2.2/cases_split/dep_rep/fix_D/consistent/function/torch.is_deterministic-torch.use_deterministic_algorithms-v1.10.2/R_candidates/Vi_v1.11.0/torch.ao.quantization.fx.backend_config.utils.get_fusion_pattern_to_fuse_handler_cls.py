def get_fusion_pattern_to_fuse_handler_cls(
        backend_config_dict: Dict[str, Any]) -> Dict[Pattern, Callable]:
    fusion_pattern_to_fuse_handlers = dict()
    for config in backend_config_dict.get("configs", []):
        if "fuser_method" in config:
            pattern = config["pattern"]
            fusion_pattern_to_fuse_handlers[pattern] = \
                get_fuse_handler_cls()

    return fusion_pattern_to_fuse_handlers
