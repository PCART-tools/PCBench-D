def _fits(doc: Doc, width: int, agenda: list[tuple[int, _BreakMode, Doc]]
         ) -> bool:
  while width >= 0 and len(agenda) > 0:
    i, m, doc = agenda.pop()
    if isinstance(doc, _NilDoc):
      pass
    elif isinstance(doc, _TextDoc):
      width -= len(doc.text)
    elif isinstance(doc, _ConcatDoc):
      agenda.extend((i, m, d) for d in reversed(doc.children))
    elif isinstance(doc, _BreakDoc):
      if m == _BreakMode.BREAK:
        return True
      width -= len(doc.text)
    elif isinstance(doc, _NestDoc):
      agenda.append((i + doc.n, m, doc.child))
    elif isinstance(doc, _GroupDoc):
      agenda.append((i, _BreakMode.FLAT, doc.child))
    elif isinstance(doc, _ColorDoc):
      agenda.append((i, m, doc.child))
    else:
      raise ValueError("Invalid document ", doc)

  return width >= 0
