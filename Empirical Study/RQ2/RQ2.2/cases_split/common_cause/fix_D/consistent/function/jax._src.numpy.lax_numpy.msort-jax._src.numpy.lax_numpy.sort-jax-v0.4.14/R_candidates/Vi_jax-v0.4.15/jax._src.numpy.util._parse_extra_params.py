def _parse_extra_params(extra_params: str) -> dict[str, str]:
  """Parse the extra parameters passed to _wraps()"""
  parameters = _parameter_break.split(extra_params.strip('\n'))
  return {p.partition(' : ')[0].partition(', ')[0]: p for p in parameters}
