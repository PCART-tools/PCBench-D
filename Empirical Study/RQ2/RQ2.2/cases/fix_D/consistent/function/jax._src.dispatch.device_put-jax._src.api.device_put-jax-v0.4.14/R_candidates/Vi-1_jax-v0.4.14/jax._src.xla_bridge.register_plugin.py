def register_plugin(
    plugin_name: str,
    *,
    priority: int = 400,
    library_path: Optional[str] = None,
    options: Optional[Mapping[str, Union[str, int, list[int], float]]] = None,
) -> None:
  """Registers a backend factory for the PJRT plugin.

  Args:
    plugin_name: the name of the plugin.
    priority: the priority this plugin should be registered in jax backends.
      Default to be 400.
    library_path: Optional. The full path to the .so file of the plugin.
      Required when the plugin is dynamically linked.
    options: Optional. It is used when creating a PJRT plugin client.
  """
  def factory():
    # Plugin may already be statically linked in some configurations.
    if not xla_client.pjrt_plugin_loaded(plugin_name):
      if library_path is None:
        raise ValueError(
            'The library path is None when trying to dynamically load the'
            ' plugin.'
        )
      xla_client.load_pjrt_plugin_dynamically(plugin_name, library_path)

    if xla_extension_version < 165:
      return xla_client.make_c_api_client(plugin_name, options)
    else:
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


  logger.debug(
      'registering PJRT plugin %s from %s', plugin_name, library_path
  )
  experimental = plugin_name not in _nonexperimental_plugins
  register_backend_factory(plugin_name, factory, priority=priority,
                           fail_quietly=False, experimental=experimental)
