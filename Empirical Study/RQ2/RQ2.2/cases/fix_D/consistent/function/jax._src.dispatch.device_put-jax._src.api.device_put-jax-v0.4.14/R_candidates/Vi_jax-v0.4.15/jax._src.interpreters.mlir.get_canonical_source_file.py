def get_canonical_source_file(frame: source_info_util.Frame) -> str:
  source_file = frame.file_name
  if config.jax_hlo_source_file_canonicalization_regex:
    source_file = re.sub(config.jax_hlo_source_file_canonicalization_regex,
                         '', source_file)
  return source_file
