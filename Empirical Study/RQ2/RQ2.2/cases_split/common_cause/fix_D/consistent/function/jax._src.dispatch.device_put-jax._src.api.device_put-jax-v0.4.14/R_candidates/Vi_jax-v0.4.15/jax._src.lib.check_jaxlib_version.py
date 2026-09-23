def check_jaxlib_version(jax_version: str, jaxlib_version: str,
                         minimum_jaxlib_version: str) -> tuple[int, ...]:
  # Regex to match a dotted version prefix 0.1.23.456.789 of a PEP440 version.
  # PEP440 allows a number of non-numeric suffixes, which we allow also.
  # We currently do not allow an epoch.
  version_regex = re.compile(r"[0-9]+(?:\.[0-9]+)*")
  date_regex = r'(\d{4})(\d{2})(\d{2})'
  def _parse_version(v: str) -> tuple[tuple[int, ...], Optional[datetime.date]]:
    m = version_regex.match(v)
    if m is None:
      raise ValueError(f"Unable to parse jaxlib version '{v}'")
    ver = tuple(int(x) for x in m.group(0).split('.'))

    m = re.search(r'dev' + date_regex, v)
    if m is None:
      return ver, None
    year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))
    date = datetime.date(year, month, day)
    return ver, date

  _jax_version, jax_date = _parse_version(jax_version)
  _minimum_jaxlib_version, _ = _parse_version(minimum_jaxlib_version)
  _jaxlib_version, jaxlib_date = _parse_version(jaxlib_version)

  if _jaxlib_version < _minimum_jaxlib_version:
    msg = (f'jaxlib is version {jaxlib_version}, but this version '
           f'of jax requires version >= {minimum_jaxlib_version}.')
    raise RuntimeError(msg)

  msg = (f'jaxlib version {jaxlib_version} is newer than and '
         f'incompatible with jax version {jax_version}. Please '
         'update your jax and/or jaxlib packages.')
  if _jaxlib_version > _jax_version:
    raise RuntimeError(msg)

  if jaxlib_date is not None and jax_date is not None and jaxlib_date > jax_date:
    raise RuntimeError(msg)

  return _jaxlib_version
