def register_pjrt_plugin_factories(plugins_from_env: str):
  """Registers backend factories for PJRT plugins.

  A backend factory will be registered for every PJRT plugin in the input
  string, in the format of 'name1:path1,name2:path2' ('name1;path1,name2;path2'
  for windows). TPU PJRT plugin will be loaded and registered separately in
  make_tpu_client.
  """

  def make_factory(name, path):
    def factory():
      xla_client.load_pjrt_plugin_dynamically(name, path)
      return xla_client.make_c_api_client(name)

    return factory

  pjrt_plugins = _get_pjrt_plugin_names_and_library_paths(plugins_from_env)
  for plugin_name, library_path in pjrt_plugins.items():
    logger.debug(
        'registering PJRT plugin %s from %s', plugin_name, library_path
    )
    # It is assumed that if a plugin is installed, then the user wants to use
    # the plugin by default. Therefore, plugins get the highest priority.
    # For a PJRT plugin, its plugin_name is the same as its platform_name.
    register_backend_factory(
        plugin_name, make_factory(plugin_name, library_path), priority=400
    )
