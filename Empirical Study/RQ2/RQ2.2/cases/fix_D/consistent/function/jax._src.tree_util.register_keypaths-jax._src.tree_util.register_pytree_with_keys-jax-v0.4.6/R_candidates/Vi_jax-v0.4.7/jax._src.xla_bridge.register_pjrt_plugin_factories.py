def register_pjrt_plugin_factories(plugins_from_env: str) -> None:
  """Registers backend factories for PJRT plugins.

  A backend factory will be registered for every PJRT plugin in the input
  string, in the format of 'name1:path1,name2:path2' ('name1;path1,name2;path2'
  for windows). The path can be a path to the plugin library or a path to the
  plugin configuration json file. The json file needs to have a "library_path"
  field for the plugin library path. It can have an optional "create_option"
  field for the options used when creating a PJRT plugin client. The value of
  "create_option" is key-value pairs. Please see xla_client._NameValueMapping
  for the supported types of values.

  TPU PJRT plugin will be loaded and registered separately in make_tpu_client.
  """

  def make_factory(name: str, path: str):
    def factory():
      if path.endswith('.json'):
        library_path, options = _get_pjrt_plugin_config(path)
      else:
        library_path = path
        options = None

      xla_client.load_pjrt_plugin_dynamically(name, library_path)
      if lib.xla_extension_version >= 134:
        return xla_client.make_c_api_client(name, options)
      else:
        if options:
          raise ValueError(
              'Setting PJRT plugin options through json file requires'
              ' jaxlib.xla_extension_version >= 134.'
          )
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
