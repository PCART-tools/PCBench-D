def _update_debug_log_modules(module_names_str: str | None):
  logging_config.disable_all_debug_logging()
  if not module_names_str:
    return
  module_names = module_names_str.split(',')
  for module_name in module_names:
    logging_config.enable_debug_logging(module_name)
