def get_canonical_source_file(file_name: str, caches: TracebackCaches) -> str:
  if file_name in caches.canonical_name_cache:
    return caches.canonical_name_cache[file_name]

  source_file = file_name
  pattern = config.hlo_source_file_canonicalization_regex.value
  if pattern:
    source_file = re.sub(pattern, '', source_file)

  caches.canonical_name_cache[file_name] = source_file
  return source_file
