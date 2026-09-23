def _get_tpu_library_path() -> str | None:
  path_from_env = os.getenv("TPU_LIBRARY_PATH")
  if path_from_env is not None:
    return path_from_env

  libtpu_module = maybe_import_libtpu()
  if libtpu_module is not None:
    if hasattr(libtpu_module, "get_library_path"):
      if xla_extension_version < 212:
        # xla_extension_version < 212 uses tpu_tracer which requires calling
        # configure_library_path.
        libtpu_module.configure_library_path()
      return libtpu_module.get_library_path()
    else:
      # TODO(b/305803029): Remove this branch around 01/2024 after the oldest
      # supported TPU has get_library_path.
      libtpu_module.configure_library_path()
      return os.getenv("TPU_LIBRARY_PATH", None)

  return None
