def _hash_xla_flags(hash_obj, extra_flag_prefixes: list[str]):
  xla_flags_to_exclude_from_cache_key = [
      "--xla_dump_compress_protos",
      "--xla_dump_module_metadata",
      "--xla_dump_max_hlo_modules",
      "--xla_dump_include_timestamp",
      "--xla_dump_hlo_pass_re",
      "--xla_dump_hlo_module_re",
      "--xla_dump_hlo_snapshots",
      "--xla_dump_fusion_visualization",
      "--xla_dump_hlo_as_url",
      "--xla_dump_hlo_as_proto",
      "--xla_dump_hlo_as_text",
      "--xla_dump_to",
      "--xla_force_host_platform_device_count",
      "--xla_dump_disable_metadata",
      "--xla_dump_hlo_pipeline_re",
      "--xla_tpu_sdc_checker_streamz_metric",
      "--xla_tpu_sdc_checker_enable_sdc_event_callbacks",
  ]

  xla_flags = []

  xla_flags_env_var = os.getenv("XLA_FLAGS")
  if xla_flags_env_var:
    xla_flags.extend(xla_flags_env_var.split())

  for arg in sys.argv:
    if arg.startswith("--xla") or any(
        arg.startswith(p) for p in extra_flag_prefixes
    ):
      xla_flags.append(arg)

  # N.B. all XLA flags that take an argument must use '=' and not a space
  # (e.g. --xla_force_host_platform_device_count=8) (I think).
  for flag in xla_flags:
    if flag.split("=")[0] in xla_flags_to_exclude_from_cache_key:
      logger.debug("Not including XLA flag in cache key: %s", flag)
      continue
    logger.debug("Including XLA flag in cache key: %s", flag)
    _hash_string(hash_obj, flag)
