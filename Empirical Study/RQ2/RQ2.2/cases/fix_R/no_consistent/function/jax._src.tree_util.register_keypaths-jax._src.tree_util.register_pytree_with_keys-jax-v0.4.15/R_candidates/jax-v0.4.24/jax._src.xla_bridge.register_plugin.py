def register_plugin(
    plugin_name: str,
    *,
    priority: int = 400,
    library_path: str | None = None,
    options: Mapping[str, str | int | list[int] | float | bool] | None = None,
    c_api: Any | None = None,
) -> Any:
  """Registers a backend factory for the PJRT plugin.

  Args:
    plugin_name: the name of the plugin.
    priority: the priority this plugin should be registered in jax backends.
      Default to be 400.
    library_path: Optional. The full path to the .so file of the plugin. The
      plugin needs to provide either the library_path or the c_api.
    options: Optional. It is used when creating a PJRT plugin client.
    c_api: Optional. The plugin can provide a PJRT C API to be registered.
  """
  def factory():
    if not xla_client.pjrt_plugin_initialized(plugin_name):
      xla_client.initialize_pjrt_plugin(plugin_name)

    if distributed.global_state.client is None:
      return xla_client.make_c_api_client(plugin_name, options, None)
    distribute_options = {
        'node_id': distributed.global_state.process_id,
        'num_nodes': distributed.global_state.num_processes,
    }
    if options is not None:
      distribute_options.update(options)
    return xla_client.make_c_api_client(
        plugin_name, distribute_options, distributed.global_state.client
    )

  if library_path and c_api:
    logger.error(
        "Both library_path and c_api are provided when registering PJRT plugin"
        " %s",
        plugin_name,
    )
    return
  if not library_path and not c_api:
    logger.error(
        "Neither library_path nor c_api provided when registering PJRT plugin"
        " %s",
        plugin_name,
    )
    return

  logger.debug(
      'registering PJRT plugin %s from %s', plugin_name, library_path
  )
  experimental = plugin_name not in _nonexperimental_plugins
  register_backend_factory(plugin_name, factory, priority=priority,
                           fail_quietly=False, experimental=experimental)
  if library_path is not None:
    c_api = xla_client.load_pjrt_plugin_dynamically(plugin_name, library_path)  # type: ignore
    xla_client.profiler.register_plugin_profiler(c_api)
  else:
    if xla_extension_version >= 236:
      assert c_api is not None
      xla_client.load_pjrt_plugin_with_c_api(plugin_name, c_api)
  return c_api
