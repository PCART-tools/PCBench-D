def get_patched_config_dict(
    config_patches: Optional[Union[str, dict[str, Any]]] = None,
) -> dict[str, Any]:
    with config.patch(config_patches):
        return config.get_config_copy()
