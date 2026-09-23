def _parse_parameters(body: str) -> dict[str, str]:
  """Parse the Parameters section of a docstring."""
  title, underline, content = body.split('\n', 2)
  assert title == 'Parameters'
  assert underline and not underline.strip('-')
  parameters = _parameter_break.split(content)
  return {p.partition(' : ')[0].partition(', ')[0]: p for p in parameters}
