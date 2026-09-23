def parse_version(v: str) -> tuple[int, ...]:
  m = _version_regex.match(v)
  if m is None:
    raise ValueError(f"Unable to parse version '{v}'")
  return tuple(int(x) for x in m.group(1).split('.'))
