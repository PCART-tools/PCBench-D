def get_trt_plugin(
    plugin_name: str,
    field_collection: List[TRTPluginFieldCollection],
    version: str,
    plugin_namespace: str = ""
) -> TRTPlugin:
    """
    Get a TensorRT plugin based on the given parameters.

    Args:
        plugin_name (str): Name of the plugin.
        field_collection (List[TRTPluginFieldCollection]): Parameters that needed
            to create a plugin using the plugin creator.
        version (str): Version of the plugin.
        plugin_namespace (str): Namespace of the plugin.

    Returns:
        A TensorRT plugin that can be added to TensorRT network as Plugin layer.
    """
    plugin_registry = trt.get_plugin_registry()
    plugin_creator = plugin_registry.get_plugin_creator(plugin_name, version, plugin_namespace)
    assert plugin_creator, f"Unabled to find plugin creator with name {plugin_name}"
    plugin = plugin_creator.create_plugin(name=plugin_name, field_collection=field_collection)

    assert plugin is not None, f"Plugin: {plugin_name} could not be fetched"
    return plugin
