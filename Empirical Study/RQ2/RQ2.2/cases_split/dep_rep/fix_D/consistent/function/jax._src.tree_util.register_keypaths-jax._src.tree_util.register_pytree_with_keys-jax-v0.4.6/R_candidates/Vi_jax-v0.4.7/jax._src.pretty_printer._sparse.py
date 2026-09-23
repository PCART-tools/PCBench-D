def _sparse(doc: Doc) -> bool:
  agenda = [doc]
  num_annotations = 0
  seen_break = False
  while len(agenda) > 0:
    doc = agenda.pop()
    if isinstance(doc, _NilDoc):
      pass
    elif isinstance(doc, _TextDoc):
      if doc.annotation is not None:
        if num_annotations >= 1 and seen_break:
          return False
        num_annotations += 1
    elif isinstance(doc, _ConcatDoc):
      agenda.extend(reversed(doc.children))
    elif isinstance(doc, _BreakDoc):
      seen_break = True
    elif isinstance(doc, _NestDoc):
      agenda.append(doc.child)
    elif isinstance(doc, _GroupDoc):
      agenda.append(doc.child)
    elif isinstance(doc, _ColorDoc):
      agenda.append(doc.child)
    else:
      raise ValueError("Invalid document ", doc)

  return True
