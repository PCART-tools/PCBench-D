class ParsedDoc(NamedTuple):
  """
  docstr: full docstring
  signature: signature from docstring.
  summary: summary from docstring.
  front_matter: front matter before sections.
  sections: dictionary of section titles to section content.
  """
  docstr: str | None
  signature: str = ""
  summary: str = ""
  front_matter: str = ""
  sections: dict[str, str] = {}
