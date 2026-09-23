class _State(NamedTuple):
  indent: int
  mode: _BreakMode
  doc: Doc
  color: _ColorState
