def _parse_numpydoc(docstr: Optional[str]) -> ParsedDoc:
  """Parse a standard numpy-style docstring.

  Args:
    docstr: the raw docstring from a function
  Returns:
    ParsedDoc: parsed version of the docstring
  """
  if docstr is None or not docstr.strip():
    return ParsedDoc(docstr)

  # Remove any :doc: directives in the docstring to avoid sphinx errors
  docstr = _docreference.sub(
    lambda match: f"{match.groups()[0]}", docstr)

  signature, body = "", docstr
  match = _numpy_signature_re.match(body)
  if match:
    signature = match.group()
    body = docstr[match.end():]

  firstline, _, body = body.partition('\n')
  body = textwrap.dedent(body.lstrip('\n'))

  match = _numpy_signature_re.match(body)
  if match:
    signature = match.group()
    body = body[match.end():]

  summary = firstline
  if not summary:
    summary, _, body = body.lstrip('\n').partition('\n')
    body = textwrap.dedent(body.lstrip('\n'))

  front_matter = ""
  body = "\n" + body
  section_list = _section_break.split(body)
  if not _section_break.match(section_list[0]):
    front_matter, *section_list = section_list
  sections = {section.split('\n', 1)[0]: section for section in section_list}

  return ParsedDoc(docstr=docstr, signature=signature, summary=summary,
                   front_matter=front_matter, sections=sections)
